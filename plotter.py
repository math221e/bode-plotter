import pyvisa
import numpy
from matplotlib.pyplot import *
import time
import control

def bodeplot(start_exp, end_exp, num_per_decade, num, den):
    print("starting plot")
    style.use("classic")

    rm = pyvisa.ResourceManager()
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
        print(str(f) + "Hz")
    
        if index % round(N/10) == 0:
            scope.write(":TIM:RANG " + str(2/f))
            scope.write(":CHAN1:RANG " + str(last_value*2))
            scope.write(":CHAN2:RANG " + str(last_value2*2))

        scope.write(":WGEN:FREQ " + str(f))
        #time.sleep(0.01)
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


    sys = control.tf(eval(num), eval(den))


    mag, p, omega = control.bode(sys, Plot=False)

    mag = 20*numpy.log(mag)
    p = p / 3.14 * 180
    omega = omega /(2*3.14)

    values = numpy.array(values)
    values_chan2 = numpy.array(values_chan2)
    db_vals = numpy.log(values / values_chan2)*20

    numpy.savetxt("channel_1_amplitude.csv", values, delimiter=";")
    numpy.savetxt("channel_2_amplitude.csv", values_chan2, delimiter=";")
    numpy.savetxt("amplitude_db.csv", db_vals, delimiter=";")
    numpy.savetxt("frequencies.csv", freqs, delimiter=";")
    numpy.savetxt("phase.csv", phase, delimiter=";")

    fig = figure(figsize=(14, 6))

    subplot(1, 2, 1)
    gca().set_title('Amplitude')
    scatter(freqs, db_vals, label="Data")
    plot(omega, mag, color="red", label="TransferFuntion")
    legend()
    xscale("log")
    subplot(1, 2, 2)
    gca().set_title('Phase')
    scatter(freqs, phase, label="Data")
    plot(omega, p, color="red", label="TransferFunction")
    legend()
    xscale("log")
    show()
