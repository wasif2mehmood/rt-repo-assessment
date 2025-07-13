import os
import csv
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openevals.llm import create_llm_as_judge

# Add root folder to sys.path to allow imports from src and other directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env in the root folder
load_dotenv()

from src.graph import build_graph
from vectorstore import load_db
from eval_prompt import HERITAGE_EVAL_PROMPT

# Initialize Heritage system
vector_store, ensemble_retriever = load_db()
graph = build_graph(ensemble_retriever)

# Initialize OpenEvals evaluator
evaluator = create_llm_as_judge(
    prompt=HERITAGE_EVAL_PROMPT,
    judge=ChatOpenAI(
        model=os.getenv("SUB_MODEL"),
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        default_headers={
            "X-Title": "Isusu",
            "HTTP-Referer": "http://localhost",
            "Content-Type": "application/json"
        },
        verbose=True,
        extra_body={"format": "openai"}
    ),
    feedback_key="heritage_correctness",
)

def load_test_cases_from_csv(csv_file="heritage_eval_dataset.csv"):
    """Load test cases from a CSV file located in the root folder."""
    test_cases = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_cases.append({
                    "inputs": row["Input"],
                    "outputs": row["Output"]
                })
        return test_cases
    except FileNotFoundError:
        print(f"Error: {csv_file} not found in the root folder.")
        return []
    except Exception as e:
        print(f"Error loading test cases: {e}")
        return []

def evaluate_heritage():
    print("Running Heritage Evaluations with Test Cases from CSV...\n")
    
    test_cases = load_test_cases_from_csv()
    if not test_cases:
        print("No test cases loaded. Exiting.")
        return
    
    results = []
    conversation_history = []
    state = {"messages": [], "summary": ""}
    config = {"configurable": {"thread_id": "eval_thread"}}
    
    for i, test in enumerate(test_cases, 1):
        conversation_history.append(test["inputs"])
        full_inputs = "\n".join(conversation_history)
        
        state["messages"].append({"role": "user", "content": test["inputs"]})
        output_state = graph.invoke(state, config)
        output = output_state["messages"][-1].content
        
        print(f"Test {i}:")
        print(f"Input: {test['inputs']}")
        print(f"Output: {output}")
        print(f"Expected: {test['outputs']}")
        try:
            eval_result = evaluator(
                inputs=full_inputs,
                outputs=output,
                reference_outputs=test['outputs']
            )
            score = eval_result.get('score', 'N/A')
            comment = eval_result.get('comment', 'Evaluation failed')
            print(f"Score: {score}")
            print(f"Comment: {comment}")
        except Exception as e:
            print(f"Evaluator error: {e}")
            score = 'N/A'
            comment = f"Evaluation failed: {str(e)}"
        print("-" * 50)
        
        results.append({
            "Test Number": i,
            "Input": test["inputs"],
            "Output": output,
            "Expected": test["outputs"],
            "Score": score,
            "Comment": comment
        })
        
        conversation_history.append(output)
        state["messages"].append({"role": "assistant", "content": output})
        if "summary" in output_state:
            state["summary"] = output_state["summary"]

    csv_file = "heritage_eval_results.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Test Number", "Input", "Output", "Expected", "Score", "Comment"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Evaluation results saved to {csv_file}")

if __name__ == "__main__":
    evaluate_heritage()