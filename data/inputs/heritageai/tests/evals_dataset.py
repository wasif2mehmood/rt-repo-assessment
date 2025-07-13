import csv

data = [
    {
        "Input": "In which state was Nok art discovered?",
        "Output": "Nok art was discovered in Kaduna State, near Jos in Plateau State."
    },
    {
        "Input": "Who discovered the Igbo-Ukwu art archaeological site?",
        "Output": "The Igbo-Ukwu art archaeological site was discovered by Thurstan Shaw."
    },
    {
        "Input": "In which state was Esie art discovered?",
        "Output": "Esie art was discovered in Kwara State, southeast of Ilorin near Offa."
    },
    {
        "Input": "What century does Ife art date back to?",
        "Output": "Ife art dates back to the 12th to 15th century AD."
    },
    {
        "Input": "Who is considered Nigeria’s most famous writer?",
        "Output": "Wole Soyinka, who won the 1986 Nobel Prize for Literature, is considered Nigeria’s most famous writer."
    }
]

csv_file = "heritage_eval_dataset.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Input", "Output"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
print(f"CSV file '{csv_file}' has been generated successfully.")
