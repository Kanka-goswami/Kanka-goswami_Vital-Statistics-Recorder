from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from datetime import datetime
import sqlite3 as sqlite


class MainApp(App):
    ctr=0
    def build(self):
        self.icon = 'love_heart_beat_256x256px.png'
        self.last_button = None

        main_layout = BoxLayout(orientation = 'vertical')
        self.solution = TextInput(background_color = 'black',
                                  foreground_color = 'white',
                                  multiline=False,
                                  font_size=36,
                                  readonly=True)
        

        main_layout.add_widget(self.solution)

        buttons = [
            [' SYS:',' DIA:',' HR:'],
            ['7','8','9'],
            ['4','5','6'],
            ['1','2','3'],
            ['ENTER','0','CLR'],
        ]

        db_buttons = ['UP','DATA','DOWN']

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                
                button = Button(
                    text = label, font_size=30, background_color='gray',
                    pos_hint= {'center_x': 0.5, 'centre_y':0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)


        h_layout = BoxLayout()
        db_btn_0 = Button(
                    text = db_buttons[0], font_size=30, background_color='gray',
                    pos_hint= {'center_x': 0.5, 'centre_y':0.5},
                )
        db_btn_1 = Button(
                    text = db_buttons[1], font_size=30, background_color='gray',
                    pos_hint= {'center_x': 0.5, 'centre_y':0.5},
                )
        db_btn_2 = Button(
                    text = db_buttons[2], font_size=30, background_color='gray',
                    pos_hint= {'center_x': 0.5, 'centre_y':0.5},
                )
        
        db_btn_0.bind(on_press=self.db_query_up)
        db_btn_1.bind(on_press=self.db_query_data)
        db_btn_2.bind(on_press=self.db_query_down)
        h_layout.add_widget(db_btn_0)
        h_layout.add_widget(db_btn_1)
        h_layout.add_widget(db_btn_2)
        main_layout.add_widget(h_layout)
            
       
        return main_layout
    


    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text
        #counter = 0
        if button_text == 'CLR':
            self.solution.text = ''
            counter=0
        elif button_text == 'ENTER':
            if current != '':
                
                self.write_to_sql(current)
                          
        else:
            new_text = current + button_text
            self.solution.text = new_text



    def write_to_sql(self,data):
        # get date and time
        dt = datetime.now()
        dt_time = str(dt)
        #Extract Numbers from string using str.translate() with str.maketrans()
        # Initialize a translation table to remove non-numeric characters
        translation_table_num = str.maketrans('', '', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        # Initialize a translation table to retain alphabets
        translation_table_str = str.maketrans('', '', '1234567890!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        # Use str.translate() with the translation table to remove non-numeric characters
        values_str = data.translate(translation_table_num)
        header_str = data.translate(translation_table_str)
        values_list = values_str.split()
        header_list = header_str.split()
        # Connect to database
        connect_to_database = sqlite.connect('VitalStats.db')
        #create a cursor
        cur = connect_to_database.cursor()
        # Push values in table
        cur.execute("""
                    INSERT INTO VITALSTATS VALUES(?,?,?,?)
        """,(dt_time[:19],values_list[0],values_list[1],values_list[2]))

        # Commit the transaction after insert
        connect_to_database.commit()

        # Close connection
        connect_to_database.close()
        self.solution.text= str('Saved in Database!')

    
    
    def db_query_data(self,instance):
        self.ctr = 0
        db_row = self.fetch_database()
        self.solution.text = str(
            str(db_row[1])+'\t'+str(db_row[2])+'\t'+str(db_row[3])+'\t'+str(db_row[4])+'\n'+
            '     DATE   '+'\t'+'  TIME  '+'\t'+'SYS'+'\t'+'DIA'+'\t'+'HR'
            )

    def db_query_up(self,instance):
        if self.ctr >= 0:
            self.ctr += 1
            db_row = self.fetch_database(self.ctr)       
        try:
            if db_row != None:
                self.solution.text = str(
                str(db_row[1])+'\t'+str(db_row[2])+'\t'+str(db_row[3])+'\t'+str(db_row[4])+'\n'+
                '     DATE   '+'\t'+'  TIME  '+'\t'+'SYS'+'\t'+'DIA'+'\t'+'HR'
                )
            else: self.solution.text = 'End of Data'
        except: print('Database Doesnot exist')
    
    def db_query_down(self,instance):
        if self.ctr >= 0 :
            self.ctr += 1
            db_row = self.fetch_database(self.ctr)      
        try:
            if db_row != None:
                self.solution.text = str(
                str(db_row[1])+'\t'+str(db_row[2])+'\t'+str(db_row[3])+'\t'+str(db_row[4])+'\n'+
                '     DATE   '+'\t'+'  TIME  '+'\t'+'SYS'+'\t'+'DIA'+'\t'+'HR'
                )
            else: self.solution.text = 'End of Data'
        except: print('Database Doesnot exist')

    def fetch_database(self,row_id = 1):
        # Connect to database
        connect_to_database = sqlite.connect('VitalStats.db')
        #create a cursor
        cur = connect_to_database.cursor()
        # Push values in table
        try:
            cur.execute("""
                    SELECT rowid, * FROM VITALSTATS WHERE rowid = ?;
                """,str(row_id))
            query = cur.fetchone()
            return query
        except: print('Data was not fetched.')

        # Close connection
        connect_to_database.close()
        





def create_database():
    # Connect to sqlite
    connect_to_database = sqlite.connect('VitalStats.db')
    
    # Create a cursor naed cur
    cur = connect_to_database.cursor()


    ## create a table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS 'VITALSTATS'(
                Date_time text,
                Systolic_mm_of_Hg text,
                Diastolic_mm_of_Hg text,
                Heart_Rate_BPM text
                );
    """)
    # commit connection
    connect_to_database.commit()

    # Close connection
    connect_to_database.close()






if __name__ == "__main__":
    create_database ()
    app = MainApp()
    app.run()
