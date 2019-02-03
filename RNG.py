from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from numpy import linspace, pi, exp
import random

#====================

# Turn interactive plotting off
plt.ioff()
# Set size of the figures in inches (DPI = 72)
plt.rcParams["figure.figsize"] = 14, 8.5

#====================

def distribution_update(*args):
    if distribution.get() == "Uniform Distribution":
        # Remove parameter fields from other distributions
        mu_label.place_forget()
        mu_field.place_forget()
        sigma_label.place_forget()
        sigma_field.place_forget()
        lamb_label.place_forget()
        lamb_field.place_forget()
        
        # Add parameter fields of chosen distribution
        a_label.place(x = 660, y = 0, width=91, height=30)
        a_field.place(x = 751, y = 0, width=91, height=30)
        b_label.place(x = 842, y = 0, width=91, height=30)
        b_field.place(x = 933, y = 0, width=91, height=30)
        
        # Change the displayed pdf formula
        pdf_img = ImageTk.PhotoImage(Image.open("uniform_pdf.png"))
        pdf_formula.config(image=pdf_img)
        pdf_formula.image = pdf_img # keep a reference!
    elif distribution.get() == "Normal Distribution":
        # Remove parameter fields from other distributions
        a_label.place_forget()
        a_field.place_forget()
        b_label.place_forget()
        b_field.place_forget()
        lamb_label.place_forget()
        lamb_field.place_forget()
        
        # Add parameter fields of chosen distribution
        mu_label.place(x = 660, y = 0, width=91, height=30)
        mu_field.place(x = 751, y = 0, width=91, height=30)
        sigma_label.place(x = 842, y = 0, width=91, height=30)
        sigma_field.place(x = 933, y = 0, width=91, height=30)
        
        # Change the displayed pdf formula
        pdf_img = ImageTk.PhotoImage(Image.open("normal_pdf.png"))
        pdf_formula.config(image=pdf_img)
        pdf_formula.image = pdf_img # keep a reference!
    elif distribution.get() == "Exponential Distribution":
        # Remove parameter fields from other distributions
        a_label.place_forget()
        a_field.place_forget()
        b_label.place_forget()
        b_field.place_forget()
        mu_label.place_forget()
        mu_field.place_forget()
        sigma_label.place_forget()
        sigma_field.place_forget()
        
        # Add parameter fields of chosen distribution
        lamb_label.place(x = 660, y = 0, width=91, height=30)
        lamb_field.place(x = 751, y = 0, width=91, height=30)
        
        # Change the displayed pdf formula
        pdf_img = ImageTk.PhotoImage(Image.open("exponential_pdf.png"))
        pdf_formula.config(image=pdf_img)
        pdf_formula.image = pdf_img # keep a reference!
    #Call the function to update the plot
    update_plot()

def update_plot(*args):
    # Make plot of the selected distribution
    plot = plt.figure()
    if distribution.get() == "Uniform Distribution":
        try:
            if a.get() >= b.get():
                messagebox.showerror("Error", "Invalid values for a and/or b!")
            else:
                plt.plot(linspace(a.get()-(b.get() - a.get())/10, a.get(), 100), [0]*100)
                plt.plot(linspace(a.get(), b.get(), 100), [1/(b.get() - a.get())]*100)
                plt.plot(linspace(b.get(), b.get()+(b.get() - a.get())/10, 100), [0]*100)
        except:
            messagebox.showerror("Error", "Invalid values for a and/or b!")
    elif distribution.get() == "Normal Distribution":
        try:
            if sigma.get() <= 0:
                messagebox.showerror("Error", "Invalid value for sigma!")
            else:
                x_axis = linspace(mu.get() - 2 * sigma.get()**2, mu.get() + 2 * sigma.get()**2, 100)
                y_axis = [1/(2 * pi * sigma.get()**2)**(1/2) * exp(- (x - mu.get())**2 / (2 * sigma.get())) for x in x_axis]
                plt.plot(x_axis, y_axis)
        except:
            messagebox.showerror("Error", "Invalid value for mu and/or sigma!")
    elif distribution.get() == "Exponential Distribution":
        try:
            if lamb.get() <= 0:
                messagebox.showerror("Error", "Invalid value for lambda!")
            else:
                x_axis = linspace(0, 1 / lamb.get() + 5, 100)
                y_axis = [lamb.get() * exp(- lamb.get() * x) for x in x_axis]
                plt.plot(x_axis, y_axis)
        except:
            messagebox.showerror("Error", "Invalid value for lambda!")
    # Save the plot as an image
    plot.savefig("distribution_plot.png")
    plt.close(plot)
    # Update the displayed distribution image
    dist_img = ImageTk.PhotoImage(Image.open("distribution_plot.png"))
    pdf_plot.config(image=dist_img)
    pdf_plot.image = dist_img # keep a reference!

#====================

# Create a window
window = Tk()
# Set the window title
window.title("Random Number Generator")
# Set window size
window.geometry("1024x768")

#====================

# Make parameters for the distributions
# Uniform Distribution
a = DoubleVar(window)
b = DoubleVar(window)
a.set(0)
b.set(1)
a_label = Label(window, text="a =")
b_label = Label(window, text="b =")
a_field = Entry(window, bd=5, textvariable=a, width=50)
b_field = Entry(window, bd=5, textvariable=b, width=50)

# Normal Distribution
mu = DoubleVar(window)
sigma = DoubleVar(window)
mu.set(0)
sigma.set(1)
mu_label = Label(window, text="mu =")
sigma_label = Label(window, text="sigma =")
mu_field = Entry(window, bd=5, textvariable=mu, width=50)
sigma_field = Entry(window, bd=5, textvariable=sigma, width=50)

# Exponential Distribution
lamb = DoubleVar(window)
lamb.set(1)
lamb_label = Label(window, text="lambda =")
lamb_field = Entry(window, bd=5, textvariable=lamb, width=50)

#====================

# Create instruction label
instr_label = Label(window, text="Choose the distribution to sample from:")
# Create exit label
exit_label = Label(window, text="Click the button to close the window:")
# Create parameter label
parameter_label = Label(window, text="Parameter(s):")

# Create distribution variable
distribution = StringVar(window)
# Set a default value
distribution.set("Uniform Distribution")
# Create dropdown to choose distribution
distribution_choice = OptionMenu(window, distribution, "Uniform Distribution", "Normal Distribution", "Exponential Distribution")

# Create field to show the pdf of the chosen distribution
pdf_formula = Label(window)
# Create field to show the plot of the pdf
pdf_plot = Label(window)
# Create button to update the plot
update_button = Button(window, text="Update plot", command=update_plot)
# Create exit button
exit_button = Button(window, text="Exit", command=window.destroy)

# Keep plot, parameters and pdf_formula updated
distribution.trace("w", distribution_update)

#====================

# Add components in wanted order to the window
instr_label.place(x = 0, y = 0, width=250, height=30)
distribution_choice.place(x = 270, y = 0, width=250, height=30)
parameter_label.place(x = 540, y = 0, width=100, height=30)
update_button.place(x = 270, y = 50, width=250, height=30)
pdf_formula.place(x = 540, y = 50, width=484, height=80)
exit_label.place(x = 0, y = 100, width=250, height=30)
exit_button.place(x = 270, y = 100, width=250, height=30)
pdf_plot.place(x = 0, y = 150, width=1024, height=618)

# Initialize the starting plot and the display of the parameters
distribution_update()

# Wait for user input
window.mainloop()