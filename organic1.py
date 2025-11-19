from manim import *
import numpy as np

ATOM_COLOR = BLUE_C
BOND_COLOR = BLUE_C

class TitleCard(Scene):
    def construct(self):
        title = Text("MODULE - 1 - ORGANIC CHEMISTRY - SOME BASIC CONCEPTS", font_size=48)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

class OrganicChemScene(Scene):
    def construct(self):
        # Heading 1: Organic chemistry definition
        heading = MarkupText("<b>Organic chemistry is the\nchemistry of carbon compounds.</b>", font_size=36)
        heading.to_edge(UP)
        self.play(Write(heading))
        # Show a big blue "C" that shrinks to a dot
        C = Text("C", font_size=96, color=BLUE)
        C.move_to(2*UP)
        self.play(FadeIn(C))
        self.play(C.animate.scale(0.08).move_to(ORIGIN))  # visually becomes small
        # Replace the shrunk C with a Dot (cyan)
        small_dot = Dot(point=ORIGIN, radius=0.08, color=ATOM_COLOR)
        self.play(Transform(C, small_dot))
        self.remove(C); self.add(small_dot)

        self.wait(0.5)

        # Change heading to catenation sentence
        new_heading = MarkupText(
            "<b>Carbon atoms have a tendency to form bonds between\ntheir own atoms to form long chains</b>",
            font_size=32
        )
        new_heading.to_edge(UP)
        self.play(Transform(heading, new_heading))

        # Create zig-zag chain (points) and animate dot moving while lines appear

        self.play(small_dot.animate.move_to(np.array([-2.8, 0, 0])), run_time=1)

        zig_points = [np.array([0,0,0])]
        length = 0.8
        for i in range(1,8):
            angle = (np.pi/6) * ((-1)**i)  # alternate up/down
            x = zig_points[-1][0] + length
            y = zig_points[-1][1] + length * np.tan(angle)
            zig_points.append(np.array([x, y, 0]))
        # shift left so centered
        offset = (zig_points[-1][0]/2) * RIGHT
        zig_points = [p - offset for p in zig_points]

        # create lines and small dots for atoms
        chain_lines = VGroup(*[Line(zig_points[i], zig_points[i+1], color=BOND_COLOR, stroke_width=4)
                               for i in range(len(zig_points)-1)])
        chain_dots = VGroup(*[Dot(p, radius=0.06, color=ATOM_COLOR) for p in zig_points])

        # animate: create lines one by one while moving a tracer dot along path
        tracer = Dot(zig_points[0], radius=0.07, color=ATOM_COLOR)
        self.add(tracer)
        for i, line in enumerate(chain_lines):
            self.play(Create(line), MoveAlongPath(tracer, line), Create(chain_dots[i+1]), run_time=0.6)
        self.remove(tracer)

        # Show catenation label under heading
        catenation = MarkupText("<i>This property is called <b>catenation</b></i>", font_size=28)
        catenation.next_to(heading, DOWN, buff=1)
        self.play(FadeIn(catenation))
        self.wait(2)
        
        self.play(FadeOut(chain_lines), FadeOut(chain_dots), FadeOut(small_dot), FadeOut(catenation))  # clear lower graphics

        # Replace heading and catenation with next statement
        heading2 = MarkupText("<b>Carbon atoms can form strong covalent bonds\nwith H, O, N, S and halogens.</b>",
                              font_size=30)
        heading2.to_edge(UP)
        self.play(Transform(heading, heading2))

        # Center C and draw five equally spaced bonds with labels
        center_C = Text("C", font_size=64, color=BLUE)
        center_C.move_to(DOWN*0.2)
        
        self.add(center_C)
        self.play(FadeIn(center_C))

        labels = ["H", "O", "N", "S", "halogens"]
        n = len(labels)
        radius = 1.6
        angles = np.linspace(90*DEGREES, 450*DEGREES, n, endpoint=False)  # start at top, spread equally

        bonds = VGroup()
        label_mobs = VGroup()
        for a, lab in zip(angles, labels):
            pos = center_C.get_center() + radius * np.array([np.cos(a), np.sin(a), 0])
            bond = Line(center_C.get_center(), pos, color=BOND_COLOR, stroke_width=4)
            label = Text(lab, font_size=28).move_to(pos + (0.25 * (pos - center_C.get_center())/np.linalg.norm(pos - center_C.get_center())))
            bonds.add(bond)
            label_mobs.add(label)

        # Animate drawing bonds and labels sequentially
        for b, l in zip(bonds, label_mobs):
            self.play(Create(b), Write(l), run_time=0.5)

        # final pause as requested
        self.wait(2)
