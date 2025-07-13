# RAG System Diagrams

This directory contains Mermaid diagrams that visualize various aspects of the RAG Assistant system architecture and implementation.

## Available Diagrams

1. **[RAG System Architecture](01_rag_system_architecture.png)** - High-level overview of the entire system showing all layers and components
2. **[Data Ingestion Pipeline](02_data_ingestion_pipeline.png)** - Detailed flow of how publication data is processed and stored
3. **[Question Answering Pipeline](03_question_answering_pipeline.png)** - Sequence diagram showing the query processing workflow
4. **[Component Interaction](04_component_interaction.png)** - How different system components interact with each other
5. **[Performance Metrics](05_performance_metrics.png)** - Visual dashboard of system performance indicators
6. **[Technology Stack](06_technology_stack.png)** - Dependencies and technologies used in the project
7. **[Project Structure](07_project_structure.png)** - Directory tree visualization of the project organization
8. **[Error Handling](08_error_handling.png)** - Error handling and recovery mechanisms

## How to Use These Diagrams

### For Development
- Use these diagrams to understand the system architecture before making changes
- Reference component interactions when debugging issues
- Check the error handling flow when implementing new features

### For Documentation
- Include rendered versions of these diagrams in presentations
- Use them in technical documentation and publications
- Share with team members to explain system design

### Rendering Options

You can render these Mermaid diagrams using:

1. **Online Tools**
   - [Mermaid Live Editor](https://mermaid.live/)
   - [GitHub's built-in rendering](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/)

2. **Local Tools**
   - VS Code with Mermaid Preview extension
   - Mermaid CLI tool for batch conversion
   - Various online converters

3. **Integration**
   - Many documentation platforms support Mermaid natively
   - CI/CD pipelines can auto-generate PNG/SVG versions
   - Include in README files for automatic rendering

## Diagram Standards

- All diagrams use consistent color coding for component types
- File names are numbered for logical ordering
- Each diagram focuses on a specific aspect of the system
- Clear labels and legends are provided where needed

## Contributing

When adding new diagrams:
- Follow the existing naming convention (XX_diagram_name.png)
- Use consistent styling and color schemes
- Include clear descriptions and legends
- Update this README with the new diagram information
