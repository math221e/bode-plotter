import pyvisa
import numpy
from matplotlib.pyplot import *
import control
import wx

def bodeplot(frame, start_exp, end_exp, num_per_decade, num, den, save_data):
    frame.SetStatusText("Starter...")
    style.use("classic")

    rm = pyvisa.ResourceManager()

    if len(rm.list_resources()) != 1:
        frame.SetStatusText("Fejl...")
        wx.MessageBox("Der blev ikke fundet noget oscilloskop. Sørg for at det er forbundet til computeren.",
                      "Fejl!",
                      wx.OK|wx.ICON_WARNING)
        frame.SetStatusText("Klar")

        return

    hideTf = False

    if den == "[1, 1]" and num == "[1]":
        hideTf = True


    scope = rm.open_resource(rm.list_resources()[0])

    scope.write_termination = "\n"
    scope.read_termination = "\n"
    scope.timeout = 5000
    scope.write(":WGEN:OUTP on")

    start_fre = int(start_exp)
    end_fre = int(end_exp)
    N = int(num_per_decade)
    freqs = numpy.logspace(start_fre, end_fre, N)
    values = []
    values_chan2 = []
    last_value = 5
    last_value2 = 5
    phase = []

    for index, f in enumerate(freqs):
        frame.SetStatusText(str(f) + "Hz")

        if index % round(N/10) == 0:
            scope.write(":TIM:RANG " + str(2/f))
            scope.write(":CHAN1:RANG " + str(last_value*2))
            scope.write(":CHAN2:RANG " + str(last_value2*2))

        scope.write(":WGEN:FREQ " + str(f))

        val = scope.query_ascii_values(":MEAS:VAMP? CHAN1", converter="f")[0]
        if val > 50:
            val = 0
    
        val2 = scope.query_ascii_values(":MEAS:VAMP? CHAN2", converter="f")[0]
        if val2 > 50:
            val2 = 0
    
        pha = scope.query_ascii_values(":MEAS:PHAS? CHAN1", converter="f")[0]
        phase.append(pha)
        values.append(val)
        values_chan2.append(val2)
        last_value = val
        last_value2 = val2



    if hideTf == False:
        sys = control.tf(eval(num), eval(den))
        mag, p, omega = control.bode(sys, Plot=False, omega=freqs*2*3.14)
        mag = 20*numpy.log(mag)
        p = p / 3.14 * 180
        omega = omega /(2*3.14)

    values = numpy.array(values)
    values_chan2 = numpy.array(values_chan2)
    db_vals = numpy.log(values / values_chan2)*20

    if save_data == True:
        numpy.savetxt("bode_data.csv", zip(freqs, db_vals, phas), delimiter=";", header="Frequency;Amplitude;Phase")

    fig = figure(figsize=(14, 6))

    subplot(1, 2, 1)
    gca().set_title('Amplitude')
    plot(freqs, db_vals, label="Data", marker=".")

    if hideTf == False:
        plot(omega, mag, color="red", label="TransferFuntion")

    legend()
    xscale("log")
    subplot(1, 2, 2)
    gca().set_title('Phase')
    plot(freqs, phase, label="Data", marker=".")

    if hideTf == False:
        plot(omega, p, color="red", label="TransferFunction")

    legend()
    xscale("log")

    frame.SetStatusText("Færdig")

    show()

    frame.SetStatusText("Klar")
