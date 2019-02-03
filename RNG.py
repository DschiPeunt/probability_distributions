from tkinter import *
from tkinter import messagebox, simpledialog
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
    sample_button.config(text="Sample from the "+distribution.get())
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


def sample_dist(*args):
    nr = simpledialog.askinteger("Input", "How many random numbers should be sampled? (Max 100000)", parent=root, minvalue=1, maxvalue=100000)
    rand_nrs = []
    if distribution.get() == "Uniform Distribution":
        try:
            if a.get() >= b.get():
                messagebox.showerror("Error", "Invalid values for a and/or b!")
            else:
                for x in range(0, nr):
                    rand_nrs.append(random.uniform(a.get(), b.get()))
        except:
            messagebox.showerror("Error", "Invalid values for a and/or b!")
    elif distribution.get() == "Normal Distribution":
        try:
            if sigma.get() <= 0:
                messagebox.showerror("Error", "Invalid value for sigma!")
            else:
                for x in range(0, nr):
                    rand_nrs.append(random.normalvariate(mu.get(), sigma.get()))
        except:
            messagebox.showerror("Error", "Invalid value for mu and/or sigma!")
    elif distribution.get() == "Exponential Distribution":
        try:
            if lamb.get() <= 0:
                messagebox.showerror("Error", "Invalid value for lambda!")
            else:
                for x in range(0, nr):
                    rand_nrs.append(random.expovariate(lamb.get()))
        except:
            messagebox.showerror("Error", "Invalid value for lambda!")
    return rand_nrs


def create_showcase_window(*args):
    rand_nrs = sample_dist()
    # Create the window and set tite and size
    showcase = Toplevel(root)
    showcase.title("Sample from the "+distribution.get())
    showcase.geometry("512x768")
    # Create button to save the sample
    save_txt_label = Label(showcase, text="Save sample to .txt file:")
    save_txt_button = Button(showcase, text="Save", command=lambda: save_to_txt(rand_nrs))
    save_txt_label.place(x = 0, y = 0, width=256, height=30)
    save_txt_button.place(x = 256, y = 0, width=256, height=30)
    # Add the generated random numbers to the window
    rand_nrs_box = Listbox(showcase, width=256, height=768)
    rand_nrs_box.place(x = 0, y = 30, width=492, height=738)
    for item in rand_nrs:
        rand_nrs_box.insert(END, item)
    # Add scrollbar
    scrollbar = Scrollbar(showcase)
    scrollbar.place(x = 492, y = 30, width=20, height=738)
    # Attach listbox (rand_nrs_box) to scrollbar
    rand_nrs_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=rand_nrs_box.yview)


def save_to_txt(rand_nrs):
    if distribution.get() == "Uniform Distribution":
        filename = "uniform" + "_a_" + str(a.get()) + "_b_" + str(b.get()) + "_sample"
    elif distribution.get() == "Normal Distribution":
        filename = "normal" + "_mu_" + str(mu.get()) + "_sigma_" + str(sigma.get()) + "_sample"
    elif distribution.get() == "Exponential Distribution":
        filename = "exponential" + "_lambda_" + str(lamb.get()) + "_sample"
    with open(filename + ".txt", "w") as f:
        for item in rand_nrs:
            f.write(str(item)+"\n")

#====================

# Create a window
root = Tk()
# Set the window title
root.title("Random Number Generator")
# Set window size
root.geometry("1024x768")

#====================

# Make parameters for the distributions
# Uniform Distribution
a = DoubleVar(root)
b = DoubleVar(root)
a.set(0)
b.set(1)
a_label = Label(root, text="a =")
b_label = Label(root, text="b =")
a_field = Entry(root, bd=5, textvariable=a, width=50)
b_field = Entry(root, bd=5, textvariable=b, width=50)

# Normal Distribution
mu = DoubleVar(root)
sigma = DoubleVar(root)
mu.set(0)
sigma.set(1)
mu_label = Label(root, text="mu =")
sigma_label = Label(root, text="sigma =")
mu_field = Entry(root, bd=5, textvariable=mu, width=50)
sigma_field = Entry(root, bd=5, textvariable=sigma, width=50)

# Exponential Distribution
lamb = DoubleVar(root)
lamb.set(1)
lamb_label = Label(root, text="lambda =")
lamb_field = Entry(root, bd=5, textvariable=lamb, width=50)

#====================

# Create text labels (instruction, sample, exit, parameter)
instr_label = Label(root, text="Choose the distribution to sample from:")
sample_label = Label(root, text="Click to sample random numbers:")
exit_label = Label(root, text="Click the button to close the window:")
parameter_label = Label(root, text="Parameter(s):")

# Create distribution variable
distribution = StringVar(root)
# Set a default value
distribution.set("Uniform Distribution")
# Create dropdown to choose distribution
distribution_choice = OptionMenu(root, distribution, "Uniform Distribution", "Normal Distribution", "Exponential Distribution")

# Create image labels to show the formula and plot of the chosen distribution
pdf_formula = Label(root)
pdf_plot = Label(root)

# Create buttons to update the plot, sample from the distribution and exit the program
update_button = Button(root, text="Update plot", command=update_plot)
sample_button = Button(root, text="Sample from the "+distribution.get(), command=create_showcase_window)
exit_button = Button(root, text="Exit", command=root.destroy)

# Keep parameters, pdf_formula, pdf_plot and sample_button updated
distribution.trace("w", distribution_update)

#====================

# Add components in wanted order to the window
# Text labels
instr_label.place(x = 0, y = 0, width=250, height=30)
sample_label.place(x = 0, y = 50, width=250, height=30)
exit_label.place(x = 0, y = 100, width=250, height=30)
parameter_label.place(x = 540, y = 0, width=100, height=30)

# Image labels
pdf_formula.place(x = 660, y = 50, width=364, height=80)
pdf_plot.place(x = 0, y = 150, width=1024, height=618)

# Buttons and Dropdown
distribution_choice.place(x = 270, y = 0, width=250, height=30)
sample_button.place(x = 270, y = 50, width=250, height=30)
exit_button.place(x = 270, y = 100, width=250, height=30)
update_button.place(x = 540, y = 50, width=100, height=30)

# Initialize the starting plot and the display of the parameters
distribution_update()

# Wait for user input
root.mainloop()