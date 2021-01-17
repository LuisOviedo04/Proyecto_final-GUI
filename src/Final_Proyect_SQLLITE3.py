from tkinter import Tk, Canvas, Frame, Label, Entry, Button, W, E, ttk, CENTER
import sqlite3

root = Tk()
root.title("PAPPENDIX 7")


def Nuevo_Calculo(KgPimientos, PHumedad, sreq, dias, Hdias, EfeColector,
                  FluAire, NMI, TMD, HumedadR, TA, frame):
    PHumedad = float(PHumedad)/100
    sreq = float(sreq)/100
    HumedadR = float(HumedadR)/100

    Humedad_inicial = float(KgPimientos) * float(PHumedad)
    Peso_seco = float(KgPimientos) - Humedad_inicial

    Humedad_Presente = (Peso_seco * float(sreq))/(1-float(sreq))

    Humedad_evaporada = Humedad_inicial - Humedad_Presente

    Insolacion_total = Peso_seco * float(dias)

    nd = (Humedad_evaporada*2320)/(float(EfeColector)*Insolacion_total*1000)
    nd = "{0:.3f}".format(nd)

    Segundos_secado = float(Hdias) * float(dias) * 3600
    np = Humedad_evaporada / (float(FluAire)*1.28*Segundos_secado*(0.0186 - 0.014))
    np = "{0:.3f}".format(np)
    conn = sqlite3.connect('SolarDryers.db')
    c = conn.cursor()

    # c.execute('''create table SolarDryersData (nd Decimal, np Decimal);''')


    query = ('''INSERT INTO SolarDryersData(nd, np) VALUES (?, ?)''')
    c.execute(query, (nd, np))
    conn.commit()
    conn.close()

    # refresh database
    display_calculos(frame)

def display_calculos(frame):
    conn = sqlite3.connect('SolarDryers.db')
    c = conn.cursor()

    #c.execute('''create table SolarDryersData (nd Decimal, np Decimal);''')

    c.execute("SELECT * FROM SolarDryersData")

    row = c.fetchall()
    Data_table = ttk.Treeview(frame, columns=2)
    Data_table.grid(row=15, column=3, columnspan=2)
    Data_table.heading("#0", text="Eficiencia de secado del sistema", anchor=CENTER)
    Data_table.heading("#1", text="Eficiencia de recogida del secador", anchor=CENTER)
    for x in row:
        Data_table.insert('', 0, text=x[0], values=x[1])
    conn.commit()
    conn.close()

# Canva
canvas = Canvas(root, height=680, width=510)
canvas.pack()

frame = Frame()
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

label = Label(frame, text="DATA INPUTS")
label.grid(row=0, column=3)

label1 = Label(frame, text="REGISTROS ALMACENADOS EN LA BASE DE DATOS")
label1.grid(row=14, column=3)

# Kg Pimientos
label = Label(frame, text="Kg Pimientos")
label.grid(row=1, column=3)
entry_KgPimientos = Entry(frame)
entry_KgPimientos.grid(row=1, column=4)
entry_KgPimientos.focus()

# % de humedad
label = Label(frame, text="% de humedad")
label.grid(row=2, column=3)
entry_PHumedad = Entry(frame)
entry_PHumedad.grid(row=2, column=4)

# % grado de sequedad requerido
label = Label(frame, text="% seq. req.")
label.grid(row=3, column=3)
entry_sreq = Entry(frame)
entry_sreq.grid(row=3, column=4)

# Días
label = Label(frame, text="Días")
label.grid(row=4, column=3)
entry_dias = Entry(frame)
entry_dias.grid(row=4, column=4)

# Horas por dia
label = Label(frame, text="Horas por dia")
label.grid(row=5, column=3)
entry_Hdias = Entry(frame)
entry_Hdias.grid(row=5, column=4)

# Efectividad del colector
label = Label(frame, text="Efe. colector")
label.grid(row=6, column=3)
entry_EfeColector = Entry(frame)
entry_EfeColector.grid(row=6, column=4)

# Flujo de aire
label = Label(frame, text="Flu. de aire")
label.grid(row=7, column=3)
entry_FluAire = Entry(frame)
entry_FluAire.grid(row=7, column=4)

# Nivel medio de insolación
label = Label(frame, text="Insolación")
label.grid(row=8, column=3)
entry_NMI = Entry(frame)
entry_NMI.grid(row=8, column=4)

# Temperatura media diaria
label = Label(frame, text="Tem. diaria")
label.grid(row=9, column=3)
entry_TMD = Entry(frame)
entry_TMD.grid(row=9, column=4)

# Humedad relativa
label = Label(frame, text="Hum. relativa")
label.grid(row=10, column=3)
entry_HumedadR = Entry(frame)
entry_HumedadR.grid(row=10, column=4)

# Temperatura del aire que ingresa
label = Label(frame, text="Tem. aire")
label.grid(row=11, column=3)
entry_TA = Entry(frame)
entry_TA.grid(row=11, column=4)


# Button
button = Button(frame, text="Calcular",
                command=lambda: Nuevo_Calculo(entry_KgPimientos.get(), entry_PHumedad.get(), entry_sreq.get(), entry_dias.get(), entry_Hdias.get(),
                                entry_EfeColector.get(), entry_FluAire.get(), entry_NMI.get(), entry_TMD.get(), entry_HumedadR.get(), entry_TA.get(), frame), bg='blue', fg='white')
button.grid(row=12, column=4, sticky=W+E)


display_calculos(frame)
root.mainloop()
