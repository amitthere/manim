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
        img = ImageMobject("AWS-AppConfig_64.png")
        # Create the rectangle
        appconfig_box = Rectangle(height=3, width=2, color=BLUE, stroke_width=2) #, fill_color="#FA4A87", fill_opacity=1)
        img.set_height(appconfig_box.height * 0.9)  # Slightly smaller than rectangle height
        img.set_width(appconfig_box.width * 0.9)  # Slightly smaller than rectangle width
        img.move_to(appconfig_box.get_center())

        # Create the label inside the box
        appconfig_label = Text("AppConfig Service", line_spacing=0.8).scale(0.5)
        appconfig_label.next_to(appconfig_box, DOWN, buff=0.3) # label below the box

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
        img.move_to(appconfig_box.get_center())
        self.add(img)
        self.play(Create(time_bar_group))

        self.wait(0.5)  # Short pause before animations start

        # --- Arrow Animation Loop ---
        # Target point for arrows (left edge of the AppConfig box is visually better)
        target_point = appconfig_box.get_critical_point(LEFT)

        # Loop through each square in the app instances grid
        for square in app_squares:
            # Starting point for the arrow (center of the current square)
            start_point = square.get_center()

            # Create an arrow Mobject. Start it small at the start_point.
            # We use a tiny initial vector (RIGHT*0.01) just to give the arrow initial direction.
            arrow = Arrow(
                start_point, start_point + RIGHT * 0.01,  # Initial small arrow at start
                buff=0.1,  # Buffer space at start/end
                color=YELLOW,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.2,  # Control tip size relative to length
                max_stroke_width_to_length_ratio=5  # Control stroke width relative to length
            )
            arrow.scale(0.8)  # Make arrows slightly smaller

            # Define the animation sequence for one arrow's round trip
            # Note: Total run_time is 1.0 second, matching the 1-second initiation interval.
            # If 8ms was intended, change run_time=0.008, but it won't be visible.
            anim_sequence = Succession(
                # 1. Create the arrow at the start point
                Create(arrow, run_time=0.1),
                # 2. Animate the arrow tip moving to the target point
                #    put_start_and_end_on ensures the arrow tail follows correctly
                arrow.animate.put_start_and_end_on(start_point, target_point),
                # 3. Brief pause at the target
                Wait(0.1),
                # 4. Animate the arrow tip moving back to the start point
                arrow.animate.put_start_and_end_on(target_point, start_point),
                # 5. Fade out the arrow once it returns
                FadeOut(arrow, run_time=0.1),
                # Total duration for the entire sequence for one arrow
                run_time=1.0
            )

            # Play the animation sequence for the current arrow
            # Since each play call waits for the previous one, and run_time is 1s,
            # a new arrow animation starts every second.
            self.play(anim_sequence)

        # Hold the final state for a bit longer after animations finish
        self.wait(2)
