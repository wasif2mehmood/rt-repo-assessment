from workflow import app, PublicationAssistantState

if __name__ == "__main__":
    # Example usage
    repo_url = input("🔗 Enter GitHub repo URL: ").strip()

    initial_state = PublicationAssistantState({
        "repo_url": repo_url,
    })

    print("\n🚀 Running Publication Assistant...\n")
    final_state = app.invoke(initial_state)

    if "final_report" in final_state:

        print("\n📝 Final Analysis Report:")
        print(final_state["final_report"].content)

        print("\n🏷️ Recommended Metadata / Keywords:")
        print(final_state["metadata_suggestions"].content)