from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# text_source = TextFileKnowledgeSource(file_paths=["file.txt"])


@CrewBase
class MedicalAssistants:
    """
    MedicalAssistants crew for diagnostic analysis

    This crew consists of two agents:
    1. Symptom Analyzer - Analyzes patient symptoms and medical data
    2. Report Creator - Creates comprehensive diagnostic reports
    3. Image Analyst - Analyzes medical images and generates insights
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def symptom_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["symptom_analyzer"],
            verbose=True,
            # knowledge_sources=[text_source],
        )

    @agent
    def report_creator(self) -> Agent:
        return Agent(config=self.agents_config["report_creator"], verbose=True)

    @task
    def analyze_symptoms(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_symptoms"],
        )

    @task
    def create_diagnostic_report(self) -> Task:
        return Task(
            config=self.tasks_config["create_diagnostic_report"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MedicalAssistants diagnostic crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
