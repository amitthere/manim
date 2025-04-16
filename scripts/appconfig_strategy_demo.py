# Install manim: pip install manim
# Run the script: manim -pql scene.py AppConfigDemoScene
# (-pql means preview, quality low)

from manim import *

class AppConfigDemoScene(Scene):
    def construct(self):
        # 1. Title
        title = Text("AppConfig Deployment Strategy Demo").scale(0.8)
        title.to_edge(UP, buff=0.5) # Place title at the top

        # 2. Table with Properties
        table_data = [
            ["Application Polling Interval","Deployment Duration","Bake Time","Growth Factor","Growth Type"],
            [ "1 second", "20 second","5 second", "20%", "LINEAR"]
        ]
        # Create the table object
        properties_table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 1, "color": WHITE}, # Style lines
            h_buff=0.5, # Horizontal buffer in cells
            v_buff=0.3,  # Vertical buffer in cells
            arrange_in_grid_config={"cell_alignment": LEFT}
        ).scale(0.45) # Scale down the table to fit
        # Position the table below the title
        properties_table.next_to(title, DOWN, buff=0.4)

        # 3. Application Instances (Grid of Squares)
        # Create 12 squares
        app_squares = VGroup(*[Square(side_length=0.7, stroke_color=WHITE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.7) for _ in range(12)])
        # Arrange them in a 3x4 grid
        app_squares.arrange_in_grid(rows=3, cols=4, buff=0.25)

        # Label for the instances
        app_instances_label = Text("Application Instances").scale(0.6)

        # Group squares and label
        app_instances_group = VGroup(app_squares, app_instances_label)
        # Arrange label below squares
        app_instances_group.arrange(DOWN, buff=0.3, center=False, aligned_edge=LEFT)
        # Position the group below the table, shifted left
        app_instances_group.next_to(properties_table, DOWN, buff=0.6)
        app_instances_group.shift(LEFT * 2.5)


        # 4. AppConfig Service Box
        # Create the rectangle
        appconfig_box = Rectangle(height=3, width=2, color=BLUE, stroke_width=2)
        # Create the label inside the box
        appconfig_label = Text("AppConfig\nService", line_spacing=0.8).scale(0.5)
        appconfig_label.move_to(appconfig_box.get_center()) # Center label in box

        # Group box and label
        appconfig_service = VGroup(appconfig_box, appconfig_label)
        # Position it to the right of the app instances group
        appconfig_service.next_to(app_instances_group, RIGHT, buff=1.5)
        # Align its top with the top of the app instances group for better layout
        appconfig_service.align_to(app_instances_group, UP)

        # 5. Time Elapsed Bar
        # Create the main horizontal line
        time_bar_line = Line(LEFT * 5, RIGHT * 5, stroke_width=2)
        # Create tick marks along the line
        ticks = VGroup(*[
            Line(UP * 0.15, DOWN * 0.15, stroke_width=2).move_to(time_bar_line.point_from_proportion(p))
            for p in [0, 0.25, 0.5, 0.75, 1] # Positions for ticks (0%, 25%, 50%, 75%, 100%)
        ])
        # Label for the time bar
        time_label = Text("Time →").scale(0.6)
        # Position the label to the left of the bar
        time_label.next_to(time_bar_line.get_start(), LEFT, buff=0.2)

        # Group line, ticks, and label
        time_bar_group = VGroup(time_label, time_bar_line, ticks)
        # Position the whole group at the bottom of the scene
        time_bar_group.to_edge(DOWN, buff=0.7)


        # Animation: Create elements on screen
        self.play(Write(title))
        self.play(Create(properties_table))
        self.play(
            LaggedStart(
                Create(app_instances_group),
                Create(appconfig_service),
                lag_ratio=0.5 # Start AppConfig service creation slightly after instances
            )
        )
        self.play(Create(time_bar_group))

        self.wait(3) # Hold the final scene for a few seconds

# if __name__ == '__main__':
#     main()
