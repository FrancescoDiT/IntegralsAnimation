from manim import *
from manim.opengl import *
import manim.utils.opengl as opengl

class ThreeDPlot(ThreeDScene):


    def function_for_plane(self, u, v, z):
        return np.array([ u , v , z])

    #crea i prismi(muretti) che stanno sotto la funzione nel dominio di integrazione
    def create_walls(self, function, dx=0.1, dy=0.1, dz=0.1):

        walls = VGroup()
        for x in np.arange(-1, 1, dx):
            for y in np.arange(-np.sqrt(1-x**2), np.sqrt(1-x**2), dy):        
                wall = Prism(dimensions=[dx, dy, function(x,y)], color=RED, fill_color=RED_B, fill_opacity=0.7, stroke_width=1)
                wall.move_to([x +dx/2 , y + dy/2, function(x,y)/2 ])
                walls.add(wall)
        return walls

    OpenGL

    def construct(self):

        def Integral_sum( function, dx=0.1, dy=0.1, dz=0.1):
            cubes = 0
            for x in np.arange(-1, 1, dx):
                for y in np.arange(-np.sqrt(1-x**2), np.sqrt(1-x**2), dy):   
                    for z in np.arange(0, function(x,y), dz):
                        cubes+=1
            return cubes*dx*dy*dz

        def math_function( x, y ):
            return  x**2 + y**2

        #def X_lower_limit():
        #    return  -1

        #def X_upper_limit():
        #    return float( 1 )

        #def Y_lower_limit( x ):
        #    return float( x**2 )

        #def Y_upper_limit( x ):
        #    return float( np.sqrt(x) )


        #dominio di visualizzazione della funzione
        u_min, u_max = -2 , 2
        v_min, v_max = -2 , 2

        
        #assi cartesiani tridimensionali
        x_min , x_max , x_step = -5 , 5 , 1
        y_min , y_max , y_step = -5 , 5 , 1
        z_min , z_max , z_step = -5 , 5 , 1
        axes = ThreeDAxes(x_range=[x_min,x_max,x_step],
                          y_range=[y_min,y_max,y_step],
                          z_range=[z_min,z_max,z_step])

        labels = axes.get_axis_labels(
                                      Text(". x-axis").scale(0.7),
                                      Text(". y-axis").scale(0.45),
                                      Text(". z-axis").scale(0.45))                            
        self.add(axes,labels)


        # Crea la superficie parametrica  
        surface = Surface(
            lambda u, v: 
            axes.c2p(*self.function_for_plane(u, v, math_function(u,v))),
            u_range=[ u_min, u_max],
            v_range=[ v_min, v_max],
            checkerboard_colors=[BLACK],
            resolution=16,
            stroke_color=RED,
            stroke_width=0.5,
            fill_opacity=1)


        d_graph = 1                                                                                  #differenziale per la generazione di Prismi
        d_calc = 100                                                                                   #differenziale per il calcolo del volume
        walls = self.create_walls(math_function, dx=1.0/d_graph, dy=1.0/d_graph, dz=1.0/d_graph)      #VGroup di Prismi
        value = Integral_sum(math_function, dx=1.0/d_calc, dy=1.0/d_calc, dz=1.0/d_calc)              #valore della somma integrale    

        
        counter = DecimalNumber(0, num_decimal_places=2, color=WHITE)           #crea un oggetto DecimalNumber per il contatore
        counter_tracker = ValueTracker(0)                                       #crea un oggetto ValueTracker per tener traccia del valore del contatore 
        counter.add_updater(lambda m: m.set_value(counter_tracker.get_value())) #collega il DecimalNumber al ValueTracker
        self.add(counter)                                                       #aggiungi il DecimalNumber alla scena


        self.set_camera_orientation(phi=60* DEGREES, theta=-45* DEGREES)        #imposto la posizione iniziale del POV
        
        rotation_rate = 0.5
        self.begin_ambient_camera_rotation(rate=rotation_rate, about="theta")                              #faccio ruotare il POV
        
        self.play(Create(walls), counter_tracker.animate.increment_value(value), run_time=5)    #eseguo le animazioni di creazione dei vari oggetti della scena

        self.play(Create(surface), run_time=2.5)
        self.wait(1.5)
        self.play(Uncreate(surface), run_time=2.5)

        self.move_camera(zoom=2, phi=80*DEGREES)


        scale_param = 4
        d_graph = d_graph*scale_param
        second_walls = self.create_walls(math_function, dx=1.0/d_graph, dy=1.0/d_graph, dz=1.0/d_graph)
        self.play(ReplacementTransform(walls, second_walls))

        d_graph = d_graph*scale_param
        third_walls = self.create_walls(math_function, dx=1.0/d_graph, dy=1.0/d_graph, dz=1.0/d_graph)
        self.play(ReplacementTransform(second_walls, third_walls))

        d_graph = d_graph*scale_param
        fourth_walls = self.create_walls(math_function, dx=1.0/d_graph, dy=1.0/d_graph, dz=1.0/d_graph)
        self.play(ReplacementTransform(third_walls, fourth_walls))


        self.move_camera(zoom=1, phi=60*DEGREES)
        

        d_graph = d_graph*scale_param
        fifth_walls = self.create_walls(math_function, dx=1.0/d_graph, dy=1.0/d_graph, dz=1.0/d_graph)
        self.play(ReplacementTransform(fourth_walls, fifth_walls))
        
        self.wait(2 * PI)                   #aspetta una rotazione completa (2 * PI)
        self.stop_ambient_camera_rotation() #fermo la rotazione del POV



        self.wait(1)

        




