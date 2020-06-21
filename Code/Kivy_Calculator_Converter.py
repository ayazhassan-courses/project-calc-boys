import math
import kivy
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner

class MainWindow(Screen):
    operators = ListProperty(["/", "*", "+", "-"])

    ##    buttons = ListProperty([
    ##                        ["9","8","7","/"],
    ##                        ["6","5","4","*"],
    ##                        ["3","2","1","-"],
    ##                        [".","0","C", "+"]])
    def on_kv_post(self, *args):
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(multiline=False, readonly=False, halign="right", font_size=60)
        main_layout.add_widget(self.solution)
        overall = BoxLayout(orientation="horizontal")
        overall_2 = BoxLayout(orientation="vertical", size_hint=(0.2, 1))
        no_colour = [".", "0", "C", "3", "2", "1", "6", "5", "4", "9", "8", "7"]
        buttons = [
            ("(", ")"),
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            (".", "0", "C", "+")]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
##                button = Button(text=label, pos_hint={"center_x": 0.5, "center_y": 0.5},
##                                background_color=[192, 192, 192, 0.3])
                if label in no_colour:
                    button = Button(text= label, pos_hint = {"center_x":0.5, "center_y":0.5}, background_color = [128, 128, 128, 0.1]) #[192,192,192,0.3])
                else:
                    button = Button(text= label, pos_hint = {"center_x":0.5, "center_y":0.5}, background_color = [0,0,255, 0.5])
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        equals_button = Button(text="=", pos_hint={"center_x": 0.5, "center_y": 0.5},
                               background_color=[128, 128, 128, 0.1])
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)
        overall.add_widget(main_layout)
        l = Label(text="History", size_hint=(1, 0.1))
        clear = Button(text="Clear", size_hint=(1, 0.08), background_color = [128, 128, 128, 0.2])
        clear.bind(on_press=self.clear_h)
        self.history = TextInput(multiline=True, readonly=True, halign="right", font_size=40)
        overall_2.add_widget(l)
        overall_2.add_widget(self.history)
        overall_2.add_widget(clear)
        overall.add_widget(overall_2)
        # self.add_widget(main_layout)
        self.ids.b_layout.add_widget(overall)

    def clear_h(self, instance):
        self.history.text = ""

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        else:
            if current and (self.last_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_operator = self.last_button in self.operators


    def on_solution(self, instance):
        def top(lst):
            return lst[len(lst)-1]

        def push(lst,item):
            lst.append(item)

        def pop(lst):
            return(lst.pop())

        def is_empty(lst):
            if lst==[]:
                return True
            else:
                return False

        def Infix_to_Postfix(expression):
            expression = expression.split()
            op_stack = []
            out = []
            finalst = ""
            for i in expression:
                if i == "(":
                    push(op_stack, i)
                elif i == ")":
                    while op_stack[-1] != "(":
                        out.append(pop(op_stack))
                    pop(op_stack)
                elif i == "/" or i == "*":
                    push(op_stack, i)
                elif i == "+" or i == "-":
                    if ((is_empty(op_stack) == False) and ((op_stack[-1] == "/") or (op_stack[-1] == "*") or (op_stack[-1] == "+") or(op_stack[-1]== "-"))):
                        while (is_empty(op_stack) == False):
                            out.append(pop(op_stack))
                    push(op_stack, i)
                else:
                    out.append(i)
            while is_empty(op_stack) == False:
                out.append(pop(op_stack))
                
            out2 = out[::-1]
            while is_empty(out2) == False:
                if len(out2) == 1:
                    finalst += pop(out2)
                else:
                    finalst += pop(out2) + " "


            return(finalst)

        def postfixEval(exp):
            exp = exp.split()
            s = 0
            lst = []
            temp = 0
            for i in exp:
                if i == "+":
                    s = float(pop(lst)) + float(pop(lst))
                    push(lst,s)
                elif i == "-":
                    y=float(pop(lst))
                    x=float(pop(lst))
                    final = x - y
                    push(lst,final)
                elif i == "*":
                    s = float(pop(lst)) * float(pop(lst))
                    push(lst,s)
                elif i == "/":
                    temp = float(pop(lst))
                    s = float(pop(lst)) / temp
                    push(lst,s)
                else:
                    push(lst,i)
            return lst[0]
        
        def fix_expression(exp):
            final = ""
            num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            for k in range(len(exp)):
                if exp[k] in num and k != (len(exp)-1) and exp[k+1] in num:
                    final += exp[k]
                else:
                    final += exp[k] + " "
            return final
        


        text = fix_expression(self.solution.text)
        self.history.text += text + "="
        if text:
            temp = Infix_to_Postfix(text)
            solution = str(postfixEval(temp))
            self.solution.text = solution
            self.history.text += solution + "\n"
            


        

##    def on_solution(self, instance):
##        text = self.solution.text
##        self.history.text += text + "="
##        if text:
##            solution = str(eval(self.solution.text))
##            self.solution.text = solution
##            self.history.text += solution + "\n"


class SecondWindow(Screen):
    operators = ListProperty(["/", "*", "+", "-"])

    def on_kv_post(self, *args):

        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(multiline=False, readonly=False, halign="right", font_size=50)
        main_layout.add_widget(self.solution)
        overall = BoxLayout(orientation="horizontal")
        overall_2 = BoxLayout(orientation="vertical", size_hint=(0.2, 1))
        no_colour = [".", "0", "C", "3", "2", "1", "6", "5", "4", "9", "8", "7"]
        buttons = [("(", ")", "1/x", "log", "+/-"),
                   ("\u03C0", "n!", "e", "ln", "%"),
                   ("2\u221A", "3\u221A", "n\u221A", "2\u207F", "Sin"),
                   ("x\u00B2", "x\u00B3", "x\u207F", "10\u207F", "Cos"),
                   ("7", "8", "9", "/", "Tan"),
                   ("4", "5", "6", "*", "Sin-1"),
                   ("1", "2", "3", "-", "Cos-1"),
                   (".", "0", "C", "+", "Tan-1")]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
##                button = Button(text=label, pos_hint={"center_x": 0.5, "center_y": 0.5},
##                                background_color=[192, 192, 192, 0.3])
                if label in no_colour:
                    button = Button(text= label, pos_hint = {"center_x":0.5, "center_y":0.5}, background_color = [128, 128, 128, 0.1]) #[192,192,192,0.3])
                else:
                    button = Button(text= label, pos_hint = {"center_x":0.5, "center_y":0.5}, background_color = [0,0,255, 0.5])#[0,0,255, 0.7] blue #[0, 51, 255,0.2]
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        equals_button = Button(text="=", pos_hint={"center_x": 0.5, "center_y": 0.5},  #, color=[192, 192, 192, 10]
                               background_color=[128, 128, 128, 0.1])
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)
        overall.add_widget(main_layout)
        l = Label(text="History", size_hint=(1, 0.1))
        clear = Button(text="Clear", size_hint=(1, 0.08), background_color = [128, 128, 128, 0.2])
        clear.bind(on_press=self.clear_h)
        self.history = TextInput(multiline=True, readonly=True, halign="right", font_size=40)
        overall_2.add_widget(l)
        overall_2.add_widget(self.history)
        overall_2.add_widget(clear)
        overall.add_widget(overall_2)
        # self.add_widget(main_layout)
        self.ids.s_layout.add_widget(overall)

    def clear_h(self, instance):
        self.history.text = ""

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        elif button_text == "\u03C0":
            self.solution.text = current + "(22/7)"
##        elif button_text == "Sin":
##            self.solution.text = str(math.sin(eval(current)))
##        elif button_text == "Cos":
##            self.solution.text = str(math.cos(eval(current)))
##        elif button_text == "Tan":
##            self.solution.text = str(math.tan(eval(current)))
        elif button_text == "n!":
            self.solution.text = str(math.factorial(eval(current)))
        elif button_text == "e":
            self.solution.text = current + str(math.e)
        elif button_text == "log":
            self.solution.text = str(math.log(eval(current), 10))
        elif button_text == "ln":
            self.solution.text = str(math.log(eval(current), math.e))
        elif button_text == "x\u00B2":
            self.solution.text = str(math.pow(eval(current), 2))
        elif button_text == "x\u00B3":
            self.solution.text = str(math.pow(eval(current), 3))
        elif button_text == "x\u207F":
            self.solution.text = current + "^"
        elif button_text == "10\u207F":
            self.solution.text = "10" + "^" + str(eval(current))
        elif button_text == "2\u221A":
            self.solution.text = str(math.pow(eval(current), 1 / 2))
        elif button_text == "3\u221A":
            self.solution.text = str(math.pow(eval(current), 1 / 3))
        elif button_text == "n\u221A":
            self.solution.text = str(eval(current)) + "under-root"
        elif button_text == "2\u207F":
            self.solution.text = str(math.pow(2, eval(current)))
        elif button_text == "%":
            self.solution.text = str(eval(current) / 100)
        elif button_text == "+/-":
            self.solution.text = str(eval(current) * -1)
        elif button_text == "1/x":
            self.solution.text = str(1 / eval(current))
        elif button_text == "Sin-1":
            if current > "1":
                self.solution.text = "Domain Error"
            else:
                self.solution.text = str(math.asin(eval(current)))
        elif button_text == "Cos-1":
            if current > "1":
                self.solution.text = "Domain Error"
            else:
                self.solution.text = str(math.acos(eval(current)))
        elif button_text == "Tan-1":
            if current > "1":
                self.solution.text = "Domain Error"
            else:
                self.solution.text = str(math.atan(eval(current)))

        else:
            if current and (self.last_operator and button_text in self.operators):
                return
            elif current == "" and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_operator = self.last_button in self.operators

    def on_solution(self, instance):
        #if ("Sin" in text) or ("Cos" in text) or ("Tan" in text):

        def top(lst):
            return lst[len(lst)-1]

        def push(lst,item):
            lst.append(item)

        def pop(lst):
            return(lst.pop())

        def is_empty(lst):
            if lst==[]:
                return True
            else:
                return False

        def Infix_to_Postfix(expression):
            expression = expression.split()
            op_stack = []
            out = []
            finalst = ""
            for i in expression:
                if i == "Sin":
                    push(op_stack, i)
                elif i == "Cos":
                    push(op_stack, i)
                elif i == "Tan":
                    push(op_stack, i)
                elif i == "(":
                    push(op_stack, i)
                elif i == ")":
                    while op_stack[-1] != "(":
                        out.append(pop(op_stack))
                    pop(op_stack)
                elif i == "^":
                    push(op_stack, i)
                elif i == "/" or i == "*":
                    push(op_stack, i)
                elif i == "+" or i == "-":
                    if ((is_empty(op_stack) == False) and ((op_stack[-1] == "/") or (op_stack[-1] == "*") or (op_stack[-1] == "+") or(op_stack[-1]== "-"))):
                        while (is_empty(op_stack) == False):
                            out.append(pop(op_stack))
                    push(op_stack, i)
                else:
                    out.append(i)
            while is_empty(op_stack) == False:
                out.append(pop(op_stack))
                
            out2 = out[::-1]
            while is_empty(out2) == False:
                if len(out2) == 1:
                    finalst += pop(out2)
                else:
                    finalst += pop(out2) + " "


            return(finalst)

        def postfixEval(exp):
            exp = exp.split()
            s = 0
            lst = []
            temp = 0
            for i in exp:
                if i == "+":
                    s = float(pop(lst)) + float(pop(lst))
                    push(lst,s)
                elif i == "-":
                    y=float(pop(lst))
                    x=float(pop(lst))
                    final = x - y
                    push(lst,final)
                elif i == "*":
                    s = float(pop(lst)) * float(pop(lst))
                    push(lst,s)
                elif i == "/":
                    temp = float(pop(lst))
                    s = float(pop(lst)) / temp
                    push(lst,s)
                elif i == "^":
                    s = float(pop(lst))
                    temp = float(pop(lst))
                    push(lst,temp**s)
                elif i == "Sin":
                    temp = float(pop(lst))
                    s = float(math.sin(temp))
                    push(lst,s)
                elif i == "Cos":
                    temp = float(pop(lst))
                    s = float(math.cos(temp))
                    push(lst,s)
                elif i == "Tan":
                    temp = float(pop(lst))
                    s = float(math.tan(temp))
                    push(tan, s)
                else:
                    push(lst,i)
            return lst[0]


        def fix_expression(exp):
            final = ""
            num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
            for k in range(len(exp)):
                if (exp[k] in num and k != (len(exp)-1) and exp[k+1] in num) or (65 <=ord(exp[k]) <=122 and k != (len(exp)-1) and 65<=ord(exp[k+1])<=122):
                    final += exp[k]
                else:
                    final += exp[k] + " "
            return final                  
        text = self.solution.text
        
        self.history.text += text + "="
        if "under-root" in text:
            new = self.solution.text.replace("under-root", "**(1/")
            new += ")"
            solution = str(eval(new))
            self.solution.text = solution
            self.history.text += solution + "\n"

        elif text:
            solv = fix_expression(text)
            temp = Infix_to_Postfix(solv)
            solution = str(postfixEval(temp))
            self.solution.text = solution
            self.history.text += solution + "\n"
##        elif text:
##            solution = str(eval(self.solution.text))
##            self.solution.text = solution
##            self.history.text += solution + "\n"


class ThirdWindow(Screen):
    ##    value_input_box = ObjectProperty()
    ##    sub_unit = ObjectProperty()
    ##    def menu_label(self, spinner):
    ##        if spinner.text == "Length":
    ##            self.sub_unit.text = "Meter (m)"
    ##            self.sub_unit.values = ('Meter (m)', 'Kilometer (km)', 'Centimeter (cm)', 'Milimeter (mm)', 'Mile (mile)', 'Yard (yd)', 'Feet (ft)', 'Inch (in)')
    ##        elif spinner.text == 'Area':
    ##            self.sub_unit.text = 'Square Meter (m[sup]2[/sup])'
    ##            self.sub_unit.values = ('Square Meter (m[sup]2[/sup])', 'Square Kilometer (km[sup]2[/sup])', 'Square Centimeter (cm[sup]2[/sup])', 'Square Milimeter (mm[sup]2[/sup])', 'Square Mile (mile[sup]2[/sup])', 'Acre (acre)', 'Hectare (ha)', 'Square Yard (yd[sup]2[/sup])', 'Square Feet (ft[sup]2[/sup])', 'Square Inch (in[sup]2[/sup])')
    ##        elif spinner.text == 'Volume':
    ##            self.sub_unit.text = 'Cubic Meter (m[sup]3[/sup])'
    ##      self.sub_unit.values = ('Cubic Meter (m[sup]3[/sup])', 'Liter (l)', 'Mililiter (ml)', 'Cubic Millimeter (mm[sup]3[/sup])', 'Tablespoon-UK (tblspn)', 'Teaspoon-UK (tspn)', 'Gallon-UK (gal)', 'Ounce-UK (oz)', 'Pint-UK (pint)', 'Quart-UK (quart)')
    ##        elif spinner.text == 'Temparature':
    ##      self.sub_unit.text = 'Celcius ([sup]o[/sup]C)'
    ##      self.sub_unit.values = ('Celcius ([sup]o[/sup]C)', 'Fahrenheit ([sup]o[/sup]F)', 'Kelvin (K)')
    ##  elif spinner.text == 'Weight':
    ##      self.sub_unit.text = 'Gram (g)'
    ##            self.sub_unit.values = ('Gram (g)', 'Kilogram (kg)', 'Miligram (mg)', 'Pound (lb)', 'Ounce (oz)', 'Tonne-UK (ton)')
    ##        elif spinner.text == 'Speed':
    ##      self.sub_unit.text = 'Meter per Second (m/s)'
    ##      self.sub_unit.values = ('Meter per Second (m/s)', 'Kilometer per Hour (km/h)', 'Mile per Hour (mile/h)', 'Feet per Minute (ft/min)', 'Feet per Second (ft/s)')
    ##  elif spinner.text == 'Time':
    ##      self.sub_unit.text = 'Seconds (s)'
    ##      self.sub_unit.values = ('Seconds (s)', 'Minute (min)', 'Hour (hr)', 'Day (day)', 'Week (wk)', 'Month (mo)', 'Year (yr)', 'Decade (dec)', 'Century (c)')
    ##
    def on_kv_post(self, *args):
        main_layout = BoxLayout(orientation="vertical")
        # time
        overall = BoxLayout(orientation="horizontal")
        time_label = Label(text="Time Conversion", size_hint=(1, 0.3))
        self.time_1_spinner = Spinner(text='Second(s)', values=(
            'Second(s)', 'Minute(min)', 'Hour(hr)', 'Day(day)', 'Week(wk)', 'Month(mo)', 'Year (yr)'), background_color = [0,0,255, 0.5])

        # self.time_1_spinner.bind(text=self.on_time_select)

        self.time1 = TextInput(multiline=False, readonly=False, halign="right", font_size=40)
        self.time_2_spinner = Spinner(text='Second(s)', values=(
            'Second(s)', 'Minute(min)', 'Hour(hr)', 'Day(day)', 'Week(wk)', 'Month(mo)', 'Year (yr)'), background_color = [0,0,255, 0.5])
        self.time2 = TextInput(multiline=False, readonly=True, halign="right", font_size=40)

        equal_t = Button(text="=", size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color = [128, 128, 128, 0.2])
        equal_t.bind(on_release=self.on_time_select)

        overall.add_widget(self.time1)
        overall.add_widget(self.time_1_spinner)
        overall.add_widget(equal_t)
        overall.add_widget(self.time2)
        overall.add_widget(self.time_2_spinner)
        main_layout.add_widget(time_label)
        main_layout.add_widget(overall)

        # Distance
        overall_1 = BoxLayout(orientation="horizontal")
        distance_label = Label(text="Distance Conversion", size_hint=(1, 0.3))
        self.distance_1_spinner = Spinner(text='Meter (m)', values=(
            'Meter (m)', 'Kilometer (km)', 'Centimeter (cm)', 'Milimeter (mm)', 'Mile (mile)', 'Feet (ft)',
            'Inch (in)'), background_color = [0,0,255, 0.5])

        self.distance1 = TextInput(multiline=False, readonly=False, halign="right", font_size=40)
        self.distance_2_spinner = Spinner(text='Meter (m)', values=(
            'Meter (m)', 'Kilometer (km)', 'Centimeter (cm)', 'Milimeter (mm)', 'Mile (mile)', 'Feet (ft)',
            'Inch (in)'), background_color = [0,0,255, 0.5])
        self.distance2 = TextInput(multiline=False, readonly=True, halign="right", font_size=40)

        equal_d = Button(text="=", size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color = [128, 128, 128, 0.2])
        equal_d.bind(on_release=self.on_distance_select)

        overall_1.add_widget(self.distance1)
        overall_1.add_widget(self.distance_1_spinner)
        overall_1.add_widget(equal_d)
        overall_1.add_widget(self.distance2)
        overall_1.add_widget(self.distance_2_spinner)
        main_layout.add_widget(distance_label)
        main_layout.add_widget(overall_1)

        # Volume
        overall_2 = BoxLayout(orientation="horizontal")
        self.volume_1_spinner = Spinner(text='Cubic Meter (m\u00B3)', values=(
            'Cubic Meter (m\u00B3)', 'Liter (l)', 'Mililiter (ml)', 'Cubic Millimeter (mm\u00B3)',
            'Gallon (gal)'), background_color = [0,0,255, 0.5])
        self.volume1 = TextInput(multiline=False, readonly=False, halign="right", font_size=40)
        self.volume_2_spinner = Spinner(text='Cubic Meter (m\u00B3)', values=(
            'Cubic Meter (m\u00B3)', 'Liter (l)', 'Mililiter (ml)', 'Cubic Millimeter (mm\u00B3)',
            'Gallon (gal)'), background_color = [0,0,255, 0.5])
        self.volume2 = TextInput(multiline=False, readonly=True, halign="right", font_size=40)

        equal_v = Button(text="=", size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color = [128, 128, 128, 0.2])
        equal_v.bind(on_release=self.on_volume_select)

        overall_2.add_widget(self.volume1)
        overall_2.add_widget(self.volume_1_spinner)
        overall_2.add_widget(equal_v)
        overall_2.add_widget(self.volume2)
        overall_2.add_widget(self.volume_2_spinner)
        volume_label = Label(text="Volume Conversion", size_hint=(1, 0.3))
        main_layout.add_widget(volume_label)
        main_layout.add_widget(overall_2)

        # Weight
        overall_3 = BoxLayout(orientation="horizontal")
        self.weight_1_spinner = Spinner(text='Gram (g)', values=(
            'Gram (g)', 'Kilogram (kg)', 'Miligram (mg)', 'Pound (lb)', 'Ounce (oz)', 'Tonne (ton)'), background_color = [0,0,255, 0.5])
        self.weight1 = TextInput(multiline=False, readonly=False, halign="right", font_size=40)
        self.weight_2_spinner = Spinner(text='Gram (g)', values=(
            'Gram (g)', 'Kilogram (kg)', 'Miligram (mg)', 'Pound (lb)', 'Ounce (oz)', 'Tonne (ton)'), background_color = [0,0,255, 0.5])
        self.weight2 = TextInput(multiline=False, readonly=True, halign="right", font_size=40)

        equal_w = Button(text="=", size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color = [128, 128, 128, 0.2])
        equal_w.bind(on_release=self.on_weight_select)

        overall_3.add_widget(self.weight1)
        overall_3.add_widget(self.weight_1_spinner)
        overall_3.add_widget(equal_w)
        overall_3.add_widget(self.weight2)
        overall_3.add_widget(self.weight_2_spinner)
        weight_label = Label(text="Weight Conversion", size_hint=(1, 0.3))
        main_layout.add_widget(weight_label)
        main_layout.add_widget(overall_3)

        # temperature
        overall_4 = BoxLayout(orientation="horizontal")
        self.temper_1_spinner = Spinner(text='Celcius (\xb0C)',
                                   values=('Celcius (\xb0C)', 'Fahrenheit (\xb0F)', 'Kelvin (K)'), background_color = [0,0,255, 0.5])
        self.temper1 = TextInput(multiline=False, readonly=False, halign="right", font_size=40)
        self.temper_2_spinner = Spinner(text='Celcius (\xb0C)',
                                   values=('Celcius (\xb0C)', 'Fahrenheit (\xb0F)', 'Kelvin (K)'), background_color = [0,0,255, 0.5])
        self.temper2 = TextInput(multiline=False, readonly=True, halign="right", font_size=40)

        equal_temper = Button(text="=", size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color = [128, 128, 128, 0.2])
        equal_temper.bind(on_release=self.on_temper_select)

        overall_4.add_widget(self.temper1)
        overall_4.add_widget(self.temper_1_spinner)
        overall_4.add_widget(equal_temper)
        overall_4.add_widget(self.temper2)
        overall_4.add_widget(self.temper_2_spinner)
        temper_label = Label(text="Temperature Conversion", size_hint=(1, 0.3))
        main_layout.add_widget(temper_label)
        main_layout.add_widget(overall_4)

        # speed
        overall_5 = BoxLayout(orientation="horizontal")
        self.speed_1_spinner = Spinner(text='Meter per Second (m/s)', values=(
            'Meter per Second (m/s)', 'Kilometer per Hour (km/h)', 'Mile per Hour (mile/h)'), background_color = [0,0,255, 0.5])
        self.speed1 = TextInput(multiline=False, readonly=False, halign="right", font_size=40)
        self.speed_2_spinner = Spinner(text='Meter per Second (m/s)', values=(
            'Meter per Second (m/s)', 'Kilometer per Hour (km/h)', 'Mile per Hour (mile/h)'), background_color = [0,0,255, 0.5])
        self.speed2 = TextInput(multiline=False, readonly=True, halign="right", font_size=40)

        equal_s = Button(text="=", size_hint=(0.8, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color = [128, 128, 128, 0.2])
        equal_s.bind(on_release=self.on_speed_select)

        overall_5.add_widget(self.speed1)
        overall_5.add_widget(self.speed_1_spinner)
        overall_5.add_widget(equal_s)
        overall_5.add_widget(self.speed2)
        overall_5.add_widget(self.speed_2_spinner)
        speed_label = Label(text="Speed Conversion", size_hint=(1, 0.3))
        main_layout.add_widget(speed_label)
        main_layout.add_widget(overall_5)
        self.ids.c_layout.add_widget(main_layout)

    # ('Second(s)', 'Minute(min)', 'Hour(hr)', 'Day(day)', 'Week(wk)', 'Month(mo)', 'Year (yr)')

    def on_time_select(self, spinner):
        if self.time_1_spinner.text == "Second(s)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = self.time1.text
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = str(float(self.time1.text) / 60)
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = str(float(self.time1.text) / 3600)
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 0.00001157409722208333465)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 0.0000016534)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 0.000000380508076156)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 0.0000000317090410959293262)

        elif self.time_1_spinner.text == "Minute(min)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = str(float(self.time1.text) * 60)
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = self.time1.text
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = str(float(self.time1.text) / 60)
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 0.000694444)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 0.0000992062857143)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 0.000022831)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 0.000001902585418569)

        elif self.time_1_spinner.text == "Hour(hr)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = str(float(self.time1.text) * 3600)
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = str(float(self.time1.text) * 60)
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = self.time1.text
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 0.0416667)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 0.00595238)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 0.00136986)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 0.00011415512510136986)

        elif self.time_1_spinner.text == "Day(day)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = str(float(self.time1.text) * 86400)
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = str(float(self.time1.text) * 1440)
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = str(float(self.time1.text) * 24)
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 1)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 0.142857)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 0.032876643423)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 0.0027397232876831892345)

        elif self.time_1_spinner.text == "Week(wk)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = str(float(self.time1.text) * 604800)
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = str(float(self.time1.text) * 10080)
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = str(float(self.time1.text) * 168)
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 7)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 1)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 0.230137)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 0.019178104350137)

        elif self.time_1_spinner.text == "Month(mo)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = str(float(self.time1.text) * 2628000)
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = str(float(self.time1.text) * 43800)
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = str(float(self.time1.text) * 730.001)
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 30.4167)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 4.34524)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 1)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 0.0833334)

        elif self.time_1_spinner.text == "Year (yr)":
            if self.time_2_spinner.text == "Second(s)":
                self.time2.text = str(float(self.time1.text) * 31540000)
            elif self.time_2_spinner.text == "Minute(min)":
                self.time2.text = str(float(self.time1.text) * 525600)
                # self.time2.text = str(eval(self.time1.text + "/60"))
            elif self.time_2_spinner.text == "Hour(hr)":
                self.time2.text = str(float(self.time1.text) * 8760)
            elif self.time_2_spinner.text == "Day(day)":
                self.time2.text = str(float(self.time1.text) * 365)

            elif self.time_2_spinner.text == "Week(wk)":
                self.time2.text = str(float(self.time1.text) * 52.1429)

            elif self.time_2_spinner.text == "Month(mo)":
                self.time2.text = str(float(self.time1.text) * 12)
            elif self.time_2_spinner.text == "Year (yr)":
                self.time2.text = str(float(self.time1.text) * 1)

    # ('Meter (m)', 'Kilometer (km)', 'Centimeter (cm)', 'Milimeter (mm)', 'Mile (mile)', 'Feet (ft)', 'Inch (in)')
    def on_distance_select(self, spinner):
        if self.distance_1_spinner.text == "Meter (m)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = self.distance1.text
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = str(float(self.distance1.text) * 0.001)
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = str(float(self.distance1.text) * 100)
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = str(float(self.distance1.text) * 1000)

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = str(float(self.distance1.text) * 0.000621371)

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = str(float(self.distance1.text) * 3.28084)
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = str(float(self.distance1.text) * 39.3701)

        elif self.distance_1_spinner.text == "Kilometer (km)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = str(float(self.distance1.text) * 1000)
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = self.distance1.text
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = str(float(self.distance1.text) * 100000)
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = str(float(self.distance1.text) * 1000000)

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = str(float(self.distance1.text) * 0.621371)

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = str(float(self.distance1.text) * 3280.84)
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = str(float(self.distance1.text) * 39370.1)

        elif self.distance_1_spinner.text == "Centimeter (cm)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = str(float(self.distance1.text) * 0.01)
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = str(float(self.distance1.text) * 0.00001)
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = self.distance1.text
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = str(float(self.distance1.text) * 10)

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = str(float(self.distance1.text) * 0.0000062137)

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = str(float(self.distance1.text) * 0.0328084)
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = str(float(self.distance1.text) * 0.393701)

        elif self.distance_1_spinner.text == "Milimeter (mm)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = str(float(self.distance1.text) * 0.001)
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = str(float(self.distance1.text) * 0.000001)
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = str(float(self.distance1.text) * 0.1)
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = self.distance1.text

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = str(float(self.distance1.text) * 0.00000062137)

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = str(float(self.distance1.text) * 0.00328084)
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = str(float(self.distance1.text) * 0.0393701)

        elif self.distance_1_spinner.text == "Mile (mile)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = str(float(self.distance1.text) * 1609.34)
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = str(float(self.distance1.text) * 1.60934)
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = str(float(self.distance1.text) * 160934)
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = str(float(self.distance1.text) * 1609340)

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = self.distance1.text

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = str(float(self.distance1.text) * 5280)
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = str(float(self.distance1.text) * 63360)

        elif self.distance_1_spinner.text == "Feet (ft)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = str(float(self.distance1.text) * 0.3048)
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = str(float(self.distance1.text) * 0.0003048)
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = str(float(self.distance1.text) * 30.48)
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = str(float(self.distance1.text) * 304.8)

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = str(float(self.distance1.text) * 0.000189394)

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = self.distance1.text
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = str(float(self.distance1.text) * 12)

        elif self.distance_1_spinner.text == "Inch (in)":
            if self.distance_2_spinner.text == "Meter (m)":
                self.distance2.text = str(float(self.distance1.text) * 0.0254)
            elif self.distance_2_spinner.text == "Kilometer (km)":
                self.distance2.text = str(float(self.distance1.text) * 0.0000254)
            elif self.distance_2_spinner.text == "Centimeter (cm)":
                self.distance2.text = str(float(self.distance1.text) * 2.54)
            elif self.distance_2_spinner.text == "Milimeter (mm)":
                self.distance2.text = str(float(self.distance1.text) * 25.4)

            elif self.distance_2_spinner.text == "Mile (mile)":
                self.distance2.text = str(float(self.distance1.text) * 0.000015783)

            elif self.distance_2_spinner.text == "Feet (ft)":
                self.distance2.text = str(float(self.distance1.text) * 0.0833333)
            elif self.distance_2_spinner.text == "Inch (in)":
                self.distance2.text = self.distance1.text

    def on_volume_select(self, spinner):
        if self.volume_1_spinner.text == "Cubic Meter (m\u00B3)":
            if self.volume_2_spinner.text == "Cubic Meter (m\u00B3)":
                self.volume2.text = self.volume1.text
            elif self.volume_2_spinner.text == "Liter (l)":
                self.volume2.text = str(float(self.volume1.text) * 1000)
            elif self.volume_2_spinner.text == "Mililiter (ml)":
                self.volume2.text = str(float(self.volume1.text) * 1000000)
            elif self.volume_2_spinner.text == "Cubic Millimeter (mm\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 1000000000)

            elif self.volume_2_spinner.text == "Gallon (gal)":
                self.volume2.text = str(float(self.volume1.text) * 219.96923151543467156)


        elif self.volume_1_spinner.text == "Liter (l)":
            if self.volume_2_spinner.text == "Cubic Meter (m\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 0.001)
            elif self.volume_2_spinner.text == "Liter (l)":
                self.volume2.text = self.volume1.text
            elif self.volume_2_spinner.text == "Mililiter (ml)":
                self.volume2.text = str(float(self.volume1.text) * 1000)
            elif self.volume_2_spinner.text == "Cubic Millimeter (mm\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 1000000)

            elif self.volume_2_spinner.text == "Gallon (gal)":
                self.volume2.text = str(float(self.volume1.text) * 0.21996923151543462671)

        elif self.volume_1_spinner.text == "Mililiter (ml)":
            if self.volume_2_spinner.text == "Cubic Meter (m\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 0.000001)
            elif self.volume_2_spinner.text == "Liter (l)":
                self.volume2.text = str(float(self.volume1.text) * 0.001)
            elif self.volume_2_spinner.text == "Mililiter (ml)":
                self.volume2.text = self.volume1.text
            elif self.volume_2_spinner.text == "Cubic Millimeter (mm\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 1000)

            elif self.volume_2_spinner.text == "Gallon (gal)":
                self.volume2.text = str(float(self.volume1.text) * 0.00021996923151411431068)

        elif self.volume_1_spinner.text == "Cubic Millimeter (mm\u00B3)":
            if self.volume_2_spinner.text == "Cubic Meter (m\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 0.000000001)
            elif self.volume_2_spinner.text == "Liter (l)":
                self.volume2.text = str(float(self.volume1.text) * 0.000001)
            elif self.volume_2_spinner.text == "Mililiter (ml)":
                self.volume2.text = str(float(self.volume1.text) * 0.001)
            elif self.volume_2_spinner.text == "Cubic Millimeter (mm\u00B3)":
                self.volume2.text = self.volume1.text

            elif self.volume_2_spinner.text == "Gallon (gal)":
                self.volume2.text = str(float(self.volume1.text) * 0.000000021996923151411431068)

        elif self.volume_1_spinner.text == "Gallon (gal)":
            if self.volume_2_spinner.text == "Cubic Meter (m\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 0.00454609)
            elif self.volume_2_spinner.text == "Liter (l)":
                self.volume2.text = str(float(self.volume1.text) * 4.54609)
            elif self.volume_2_spinner.text == "Mililiter (ml)":
                self.volume2.text = str(float(self.volume1.text) * 4546.09)
            elif self.volume_2_spinner.text == "Cubic Millimeter (mm\u00B3)":
                self.volume2.text = str(float(self.volume1.text) * 4546000)

            elif self.volume_2_spinner.text == "Gallon (gal)":
                self.volume2.text = self.volume1.text

    def on_weight_select(self, spinner):
        if self.weight_1_spinner.text == "Gram (g)":
            if self.weight_2_spinner.text == "Gram (g)":
                self.weight2.text = self.weight1.text
            elif self.weight_2_spinner.text == "Kilogram (kg)":
                self.weight2.text = str(float(self.weight1.text) * 0.001)
            elif self.weight_2_spinner.text == "Miligram (mg)":
                self.weight2.text = str(float(self.weight1.text) * 1000)
            elif self.weight_2_spinner.text == "Pound (lb)":
                self.weight2.text = str(float(self.weight1.text) * 0.00220462)
            elif self.weight_2_spinner.text == "Ounce (oz)":
                self.weight2.text = str(float(self.weight1.text) * 0.035274)
            elif self.weight_2_spinner.text == "Tonne (ton)":
                self.weight2.text = str(float(self.weight1.text) * 0.00000098421)

        elif self.weight_1_spinner.text == "Kilogram (kg)":
            if self.weight_2_spinner.text == "Gram (g)":
                self.weight2.text = str(float(self.weight1.text) * 1000)
            elif self.weight_2_spinner.text == "Kilogram (kg)":
                self.weight2.text = self.weight1.text
            elif self.weight_2_spinner.text == "Miligram (mg)":
                self.weight2.text = str(float(self.weight1.text) * 1000000)
            elif self.weight_2_spinner.text == "Pound (lb)":
                self.weight2.text = str(float(self.weight1.text) * 2.20462)

            elif self.weight_2_spinner.text == "Ounce (oz)":
                self.weight2.text = str(float(self.weight1.text) * 35.274)
            elif self.weight_2_spinner.text == "Tonne (ton)":
                self.weight2.text = str(float(self.weight1.text) * 0.000984207)

        elif self.weight_1_spinner.text == "Miligram (mg)":
            if self.weight_2_spinner.text == "Gram (g)":
                self.weight2.text = str(float(self.weight1.text) * 0.001)
            elif self.weight_2_spinner.text == "Kilogram (kg)":
                self.weight2.text = str(float(self.weight1.text) * 0.000001)
            elif self.weight_2_spinner.text == "Miligram (mg)":
                self.weight2.text = self.weight1.text
            elif self.weight_2_spinner.text == "Pound (lb)":
                self.weight2.text = str(float(self.weight1.text) * 0.00000220462)

            elif self.weight_2_spinner.text == "Ounce (oz)":
                self.weight2.text = str(float(self.weight1.text) * 0.000035274)
            elif self.weight_2_spinner.text == "Tonne (ton)":
                self.weight2.text = str(float(self.weight1.text) * 0.000000000984207)

        elif self.weight_1_spinner.text == "Pound (lb)":
            if self.weight_2_spinner.text == "Gram (g)":
                self.weight2.text = str(float(self.weight1.text) * 453.592)
            elif self.weight_2_spinner.text == "Kilogram (kg)":
                self.weight2.text = str(float(self.weight1.text) * 0.453592)
            elif self.weight_2_spinner.text == "Miligram (mg)":
                self.weight2.text = str(float(self.weight1.text) * 453592)
            elif self.weight_2_spinner.text == "Pound (lb)":
                self.weight2.text = self.weight1.text

            elif self.weight_2_spinner.text == "Ounce (oz)":
                self.weight2.text = str(float(self.weight1.text) * 16)
            elif self.weight_2_spinner.text == "Tonne (ton)":
                self.weight2.text = str(float(self.weight1.text) * 0.000446429)

        elif self.weight_1_spinner.text == "Ounce (oz)":
            if self.weight_2_spinner.text == "Gram (g)":
                self.weight2.text = str(float(self.weight1.text) * 28.3495)
            elif self.weight_2_spinner.text == "Kilogram (kg)":
                self.weight2.text = str(float(self.weight1.text) * 0.028349500000294)
            elif self.weight_2_spinner.text == "Miligram (mg)":
                self.weight2.text = str(float(self.weight1.text) * 28349.500000294003257)
            elif self.weight_2_spinner.text == "Pound (lb)":
                self.weight2.text = str(float(self.weight1.text) * 0.0625)

            elif self.weight_2_spinner.text == "Ounce (oz)":
                self.weight2.text = self.weight1.text
            elif self.weight_2_spinner.text == "Tonne (ton)":
                self.weight2.text = str(float(self.weight1.text) * 0.000027902)

        elif self.weight_1_spinner.text == "Tonne (ton)":
            if self.weight_2_spinner.text == "Gram (g)":
                self.weight2.text = str(float(self.weight1.text) * 1016000)
            elif self.weight_2_spinner.text == "Kilogram (kg)":
                self.weight2.text = str(float(self.weight1.text) * 1016.05)
            elif self.weight_2_spinner.text == "Miligram (mg)":
                self.weight2.text = str(float(self.weight1.text) * 1016000000)
            elif self.weight_2_spinner.text == "Pound (lb)":
                self.weight2.text = str(float(self.weight1.text) * 2240)

            elif self.weight_2_spinner.text == "Ounce (oz)":
                self.weight2.text = str(float(self.weight1.text) * 35840)
            elif self.weight_2_spinner.text == "Tonne (ton)":
                self.weight2.text = self.weight1.text

#('Celcius (\xb0C)', 'Fahrenheit (\xb0F)', 'Kelvin (K)'))

    def on_temper_select(self, spinner):
        if self.temper_1_spinner.text == "Celcius (\xb0C)":
            if self.temper_2_spinner.text == "Celcius (\xb0C)":
                self.temper2.text = self.temper1.text
            elif self.temper_2_spinner.text == "Fahrenheit (\xb0F)":
                self.temper2.text = str(float(self.temper1.text) * (9/5) + 32)
            elif self.temper_2_spinner.text == "Kelvin (K)":
                self.temper2.text = str(float(self.temper1.text) + 273.15)

        elif self.temper_1_spinner.text == "Fahrenheit (\xb0F)":
            if self.temper_2_spinner.text == "Celcius (\xb0C)":
                self.temper2.text = str((float(self.temper1.text) - 32)* 5/9)
            elif self.temper_2_spinner.text == "Fahrenheit (\xb0F)":
                self.temper2.text = self.temper1.text
            elif self.temper_2_spinner.text == "Kelvin (K)":
                self.temper2.text = str((float(self.temper1.text)+ 459.67) * 5/9)

        elif self.temper_1_spinner.text == "Kelvin (K)":
            if self.temper_2_spinner.text == "Celcius (\xb0C)":
                self.temper2.text = str(float(self.temper1.text) - 273.15)
            elif self.temper_2_spinner.text == "Fahrenheit (\xb0F)":
                self.temper2.text = str((float(self.temper1.text) * 9/5) - 459.67)
            elif self.temper_2_spinner.text == "Kelvin (K)":
                self.temper2.text = self.temper1.text

#('Meter per Second (m/s)', 'Kilometer per Hour (km/h)', 'Mile per Hour (mile/h)')
    def on_speed_select(self, spinner):
        if self.speed_1_spinner.text == "Meter per Second (m/s)":
            if self.speed_2_spinner.text == "Meter per Second (m/s)":
                self.speed2.text = self.speed1.text
            elif self.speed_2_spinner.text == "Kilometer per Hour (km/h)":
                self.speed2.text = str(float(self.speed1.text) * 3.6)
            elif self.speed_2_spinner.text == "Mile per Hour (mile/h)":
                self.speed2.text = str(float(self.speed1.text) * 2.23694)

        elif self.speed_1_spinner.text == "Kilometer per Hour (km/h)":
            if self.speed_2_spinner.text == "Meter per Second (m/s)":
                self.speed2.text = str(float(self.speed1.text) * 0.277778)
            elif self.speed_2_spinner.text == "Kilometer per Hour (km/h)":
                self.speed2.text = self.speed1.text
            elif self.speed_2_spinner.text == "Mile per Hour (mile/h)":
                self.speed2.text = str(float(self.speed1.text) * 0.621371)

        elif self.speed_1_spinner.text == "Mile per Hour (mile/h)":
            if self.speed_2_spinner.text == "Meter per Second (m/s)":
                self.speed2.text = str(float(self.speed1.text) * 0.44704)
            elif self.speed_2_spinner.text == "Kilometer per Hour (km/h)":
                self.speed2.text = str(float(self.speed1.text) * 1.60934)
            elif self.speed_2_spinner.text == "Mile per Hour (mile/h)":
                self.speed2.text = self.speed1.text
            


class WindowManager(ScreenManager):
    pass


kivy_file = Builder.load_file("Design_b_end.kv")


class Calculator_mod(App):
    def build(self):
        return kivy_file


if __name__ == "__main__":
    app = Calculator_mod()
    app.run()
