import pyvisa
import numpy
from matplotlib.pyplot import *
import control
import wx

def bodeplot(frame, start_exp, end_exp, num_per_decade, num, den, save_data):
    frame.SetStatusText("Vent...")
    style.use("classic")

    rm = pyvisa.ResourceManager()

    if len(rm.list_resources()) != 1:
        frame.SetStatusText("Fejl...")
        wx.MessageBox("Der blev ikke fundet noget oscilloskop. Sørg for at det er forbundet til computeren.",
                      "Fejl!",
                      wx.OK|wx.ICON_WARNING)
        frame.SetStatusText("Klar")

        return

    if int(start_exp) > int(end_exp):
        frame.SetStatusText("Fejl...")
        wx.MessageBox("Start frekvens skal være mindre end slut frekvens",
                      "Fejl!",
                      wx.OK|wx.ICON_WARNING)
        frame.SetStatusText("Klar")

        return

    # if int(start_exp) >= 1 and int(start_exp) <= 6 and int(end_exp) >= 1 and int(end_exp) <= 6:
    #     frame.SetStatusText("Fejl...")
    #     wx.MessageBox("Start og steop frekvens skal være mellem 10^1 og 10^6",
    #                   "Fejl!",
    #                   wx.OK|wx.ICON_WARNING)
    #     frame.SetStatusText("Klar")

    #     return

    hideTf = False

    if den == "[1, 1]" and num == "[1]":
        hideTf = True


    scope = rm.open_resource(rm.list_resources()[0])

    scope.write_termination = "\n"
    scope.read_termination = "\n"
    scope.timeout = 20000

    start_fre = int(start_exp)
    end_fre = int(end_exp)
    N = int(num_per_decade)
    freqs = numpy.logspace(start_fre, end_fre, int((end_fre - start_fre) * N))
    channel1_vamps = []
    channel2_vamps = []
    phase = []

    scope.write(":WGEN:OUTP on")
    scope.write(":TIM:RANG " + str(2/freqs[0]))

    channel1_initial_vamp = scope.query_ascii_values(":MEAS:VPP? CHAN1", converter="f")[0]
    channel2_initial_vamp = scope.query_ascii_values(":MEAS:VPP? CHAN2", converter="f")[0]
    print(channel1_initial_vamp)
    scope.write(":CHAN1:RANG " + str(channel1_initial_vamp*2))
    scope.write(":CHAN2:RANG " + str(channel2_initial_vamp*2))

    for index, f in enumerate(freqs):
        #if index % round(N/10) == 0:
        if index > 0:
            scope.write(":TIM:RANG " + str(2/f))
            scope.write(":CHAN1:RANG " + str(channel1_vamps[-1]*3))
            scope.write(":CHAN2:RANG " + str(channel2_vamps[-1]*3))

        scope.write(":WGEN:FREQ " + str(f))

        channel1 = scope.query_ascii_values(":MEAS:VPP? CHAN1", converter="f")[0]
        if channel1 > 50:
            print(channel1)
            exit()
            #channel1 = channel1_vamps[-1]
            channel1 = 0
    
        channel2 = scope.query_ascii_values(":MEAS:VPP? CHAN2", converter="f")[0]
        if channel2 > 50:
            channel2 = channel2_vamps[-1]
    
        pha = scope.query_ascii_values(":MEAS:PHAS? CHAN1", converter="f")[0]

        if abs(pha) > 300:
            pha = False

        phase.append(pha)
        channel1_vamps.append(channel1)
        channel2_vamps.append(channel2)



    if hideTf == False:
        sys = control.tf(eval(num), eval(den))
        mag, p, omega = control.bode(sys, Plot=False, omega=freqs*2*3.14)
        mag = 20*numpy.log(mag)
        p = p / 3.14 * 180
        omega = omega /(2*3.14)

    channel1_vamps = numpy.array(channel1_vamps)
    channel2_vamps = numpy.array(channel2_vamps)

    amplitude_db = numpy.log(channel1_vamps / channel2_vamps)*20

    if save_data == True:
        with open("bode_data.csv", "w") as file:
            file.write("Frequency;Amplitude;Phase\n")

            for index, item in enumerate(freqs):
                file.write(str(freqs[index]) + ";" + str(amplitude_db[index]) + ";" + str(phase[index]) + "\n")

    fig = figure(figsize=(14, 6))
    fig.suptitle("Bode plot", fontsize=22)

    subplot(1, 2, 1)
    #gca().set_title('Amplitude')
    plot(freqs, amplitude_db, label="Data", marker=".")
    xlabel("Frequency [Hz]")
    ylabel("Amplitude [dB]")
    
    if hideTf == False:
        plot(omega, mag, color="red", label="TransferFuntion")

    legend()
    xscale("log")
    subplot(1, 2, 2)
    #gca().set_title('Phase')
    plot(freqs, phase, label="Data", marker=".")
    xlabel("Frequency [Hz]")
    ylabel("Phase [Degrees]")

    if hideTf == False:
        plot(omega, p, color="red", label="TransferFunction")

    legend()
    xscale("log")

    frame.SetStatusText("Færdig")

    show()

    frame.SetStatusText("Klar")
