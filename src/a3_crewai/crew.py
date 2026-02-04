from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool, DallETool

from a3_crewai.tools.FreesoundTool import FreesoundTool


@CrewBase
class GameBuilderCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Shared tools
    file_writer = FileWriterTool()
    dalle_tool = DallETool()

    @agent
    def ui_css_agent(self) -> Agent:
        return Agent(config=self.agents_config['ui_css_agent'])

    @agent
    def game_logic_agent(self) -> Agent:
        return Agent(config=self.agents_config['game_logic_agent'])

    @agent
    def user_input_agent(self) -> Agent:
        return Agent(config=self.agents_config['user_input_agent'])

    @agent
    def image_assets_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['image_assets_agent'],
            tools=[self.file_writer, self.dalle_tool]
        )

    @agent
    def audio_assets_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['audio_assets_agent'],
            tools=[FreesoundTool()],
        )

    @agent
    def asset_integrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['asset_integrator_agent'],
            tools=[self.file_writer]
        )

    @agent
    def template_integrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['template_integrator_agent'],
            tools=[self.file_writer]
        )

    @agent
    def reviewer_agent(self) -> Agent:
        return Agent(config=self.agents_config['reviewer_agent'])

    @agent
    def final_html_builder_agent(self) -> Agent:
        return Agent(config=self.agents_config['final_html_builder_agent'], tools=[self.file_writer])

    @task
    def ui_css_generation(self) -> Task:
        return Task(config=self.tasks_config['ui_css_generation'], agent=self.ui_css_agent())

    @task
    def game_logic_generation(self) -> Task:
        return Task(config=self.tasks_config['game_logic_generation'], agent=self.game_logic_agent())

    @task
    def user_input_generation(self) -> Task:
        return Task(config=self.tasks_config['user_input_generation'], agent=self.user_input_agent())

    @task
    def generate_image_assets(self) -> Task:
        return Task(config=self.tasks_config['generate_image_assets'], agent=self.image_assets_agent())

    @task
    def generate_audio_assets(self) -> Task:
        return Task(config=self.tasks_config['generate_audio_assets'], agent=self.audio_assets_agent())

    @task
    def integrate_assets(self) -> Task:
        return Task(config=self.tasks_config['integrate_assets'], agent=self.asset_integrator_agent())

    @task
    def template_integration(self) -> Task:
        return Task(config=self.tasks_config['template_integration'], agent=self.template_integrator_agent())

    @task
    def testing_and_debugging(self) -> Task:
        return Task(config=self.tasks_config['testing_and_debugging'], agent=self.reviewer_agent())

    @task
    def final_html_building(self) -> Task:
        return Task(config=self.tasks_config['final_html_building'], agent=self.final_html_builder_agent())

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.ui_css_agent(),
                self.game_logic_agent(),
                self.user_input_agent(),
                self.image_assets_agent(),
                self.audio_assets_agent(),
                self.asset_integrator_agent(),
                self.template_integrator_agent(),
                self.reviewer_agent(),
                self.final_html_builder_agent()
            ],
            tasks=[
                self.ui_css_generation(),
                self.game_logic_generation(),
                self.user_input_generation(),
                self.generate_image_assets(),
                self.generate_audio_assets(),
                self.integrate_assets(),
                self.template_integration(),
                self.testing_and_debugging(),
                self.final_html_building()
            ],
            process=Process.sequential,
            verbose=True,
        )
        
    


