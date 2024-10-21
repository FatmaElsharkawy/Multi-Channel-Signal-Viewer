import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button

class DraggableRectangle:
    def __init__(self, ax):
        self.ax = ax
        self.rect_selector = None  # Initialize without the RectangleSelector
        self.rectangles = []  # List to store created rectangles

    def on_select(self, eclick, erelease):
        # Function to handle rectangle selection
        print(f"Start: ({eclick.xdata}, {eclick.ydata})")
        print(f"End: ({erelease.xdata}, {erelease.ydata})")

        # Create a rectangle from the selection
        rect = plt.Rectangle(
            (eclick.xdata, eclick.ydata), 
            erelease.xdata - eclick.xdata, 
            erelease.ydata - eclick.ydata, 
            
            facecolor='red',  # Fill the rectangle with red color
            alpha=0.5  # Set transparency
        )
        self.ax.add_patch(rect)  # Add the rectangle to the axis
        self.rectangles.append(rect)  # Store the rectangle reference
        plt.draw()  # Update the plot
        
        # Deactivate the selector
        self.deactivate_selector()

    def activate_selector(self, event):
        """This function activates the RectangleSelector when called."""
        if self.rect_selector is None:  # Create it only once
            self.rect_selector = RectangleSelector(
                self.ax, 
                onselect=self.on_select, 
                interactive=True  # Make the rectangle draggable and resizable
            )
            print(f"RectangleSelector activated on {self.ax.get_title()}.")
        else:
            self.rect_selector.set_active(True)  # Re-activate if already created

    # def deactivate_selector(self):
    #     """Deactivate the rectangle selector."""
    #     if self.rect_selector is not None:
    #         self.rect_selector.set_active(False)  # Deactivate the selector
    #         print(f"RectangleSelector deactivated on {self.ax.get_title()}.")

    def clear_rectangles(self):
        """Remove all created rectangles from the axis."""
        for rect in self.rectangles:
            rect.remove()  # Remove the rectangle from the plot
        self.rectangles.clear()  # Clear the list of rectangles
        plt.draw() 

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# Plot some data on the first graph (ax1)
x = [1, 2, 3, 4, 5]
y1 = [2, 3, 4, 5, 6]
ax1.plot(x, y1)
ax1.set_title('Graph 1')

# Plot some data on the second graph (ax2)
y2 = [1, 4, 2, 5, 3]
ax2.plot(x, y2)
ax2.set_title('Graph 2')

# Instantiate DraggableRectangle for each graph
draggable_rect1 = DraggableRectangle(ax1)
draggable_rect2 = DraggableRectangle(ax2)

# Create buttons for each graph
ax_button1 = plt.axes([0.1, 0.05, 0.2, 0.075])  # Button position for the first graph
button1 = Button(ax_button1, 'Activate Graph 1')
button1.on_clicked(draggable_rect1.activate_selector)

ax_button2 = plt.axes([0.4, 0.05, 0.2, 0.075])  # Button position for the second graph
button2 = Button(ax_button2, 'Activate Graph 2')
button2.on_clicked(draggable_rect2.activate_selector)

# Create a deactivate button for both graphs
ax_deactivate = plt.axes([0.7, 0.05, 0.2, 0.075])  # Button position for deactivating both
deactivate_button = Button(ax_deactivate, 'Deactivate Both Rectangles')

def deactivate_both_rectangles(event):
    # Deactivate the selectors before clearing rectangles
    # draggable_rect1.deactivate_selector()
    # draggable_rect2.deactivate_selector()
    
    # Call the clear method for both rectangles
    draggable_rect1.clear_rectangles()
    draggable_rect2.clear_rectangles()

    # # Re-enable the activate buttons (optional, just UI update)
    # button1.label.set_text('Activate Graph 1')
    # button2.label.set_text('Activate Graph 2')
    
    plt.draw()  # Ensure the plot refreshes completely

deactivate_button.on_clicked(deactivate_both_rectangles)

plt.tight_layout()
plt.show()
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, Button

# class DraggableRectangle:
#     def __init__(self, ax):
#         self.ax = ax
#         self.rect_selector = None  # Initialize without the RectangleSelector
#         self.rectangles = []  # List to store created rectangles

#     def on_select(self, eclick, erelease):
#         # Function to handle rectangle selection
#         print(f"Start: ({eclick.xdata}, {eclick.ydata})")
#         print(f"End: ({erelease.xdata}, {erelease.ydata})")

#         # Create a rectangle from the selection
#         rect = plt.Rectangle(
#             (eclick.xdata, eclick.ydata), 
#             erelease.xdata - eclick.xdata, 
#             erelease.ydata - eclick.ydata, 
#             edgecolor='red', 
#             facecolor='red',  # Fill the rectangle with red color
#             alpha=0.5  # Set transparency
#         )
#         self.ax.add_patch(rect)  # Add the rectangle to the axis
#         self.rectangles.append(rect)  # Store the rectangle reference
#         plt.draw()  # Update the plot
        
#         # Deactivate the selector
#         self.deactivate_selector()

#     def activate_selector(self, event):
#         """This function activates the RectangleSelector when called."""
#         if self.rect_selector is None:  # Create it only once
#             self.rect_selector = RectangleSelector(
#                 self.ax, 
#                 onselect=self.on_select, 
#                 interactive=True  # Make the rectangle draggable and resizable
#             )
#             print(f"RectangleSelector activated on {self.ax.get_title()}.")
#         else:
#             self.rect_selector.set_active(True)  # Re-activate if already created

#     def deactivate_selector(self):
#         """Deactivate the rectangle selector."""
#         if self.rect_selector is not None:
#             self.rect_selector.set_active(False)  # Deactivate the selector
#             print(f"RectangleSelector deactivated on {self.ax.get_title()}.")

#     def clear_rectangles(self):
#         """Remove all created rectangles from the axis."""
#         for rect in self.rectangles:
#             rect.remove()  # Remove the rectangle from the plot
#         self.rectangles.clear()  # Clear the list of rectangles
#         plt.draw()  # Update the plot
#         print(f"All rectangles removed from {self.ax.get_title()}.")

# # Create a figure with two subplots
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# # Plot some data on the first graph (ax1)
# x = [1, 2, 3, 4, 5]
# y1 = [2, 3, 4, 5, 6]
# ax1.plot(x, y1)
# ax1.set_title('Graph 1')

# # Plot some data on the second graph (ax2)
# y2 = [1, 4, 2, 5, 3]
# ax2.plot(x, y2)
# ax2.set_title('Graph 2')

# # Instantiate DraggableRectangle for each graph
# draggable_rect1 = DraggableRectangle(ax1)
# draggable_rect2 = DraggableRectangle(ax2)

# # Create buttons for each graph
# ax_button1 = plt.axes([0.1, 0.05, 0.2, 0.075])  # Button position for the first graph
# button1 = Button(ax_button1, 'Activate Graph 1')
# button1.on_clicked(draggable_rect1.activate_selector)

# ax_button2 = plt.axes([0.4, 0.05, 0.2, 0.075])  # Button position for the second graph
# button2 = Button(ax_button2, 'Activate Graph 2')
# button2.on_clicked(draggable_rect2.activate_selector)

# # Create a deactivate button for both graphs
# ax_deactivate = plt.axes([0.7, 0.05, 0.2, 0.075])  # Button position for deactivating both
# deactivate_button = Button(ax_deactivate, 'Deactivate Both Rectangles')

# def deactivate_both_rectangles(event):
#     # Call the clear method for both rectangles
#     draggable_rect1.clear_rectangles()
#     draggable_rect2.clear_rectangles()

#     # Reset the state of both rectangle selectors
#     draggable_rect1.deactivate_selector()
#     draggable_rect2.deactivate_selector()

#     # Re-enable the activate buttons
#     button1.label.set_text('Activate Graph 1')
#     button2.label.set_text('Activate Graph 2')

# deactivate_button.on_clicked(deactivate_both_rectangles)

# plt.tight_layout()
# plt.show()
# import matplotlib.pyplot as plt
# from matplotlib.widgets import RectangleSelector, Button

# class DraggableRectangle:
#     def __init__(self, ax):
#         self.ax = ax
#         self.rect_selector = None  # Initialize without the RectangleSelector
#         self.rectangles = []  # List to store created rectangles

#     def on_select(self, eclick, erelease):
#         # Function to handle rectangle selection
#         print(f"Start: ({eclick.xdata}, {eclick.ydata})")
#         print(f"End: ({erelease.xdata}, {erelease.ydata})")

#         # Create a rectangle from the selection
#         rect = plt.Rectangle(
#             (eclick.xdata, eclick.ydata), 
#             erelease.xdata - eclick.xdata, 
#             erelease.ydata - eclick.ydata, 
#             edgecolor='red', 
#             facecolor='red',  # Fill the rectangle with red color
#             alpha=0.5  # Set transparency
#         )
#         self.ax.add_patch(rect)  # Add the rectangle to the axis
#         self.rectangles.append(rect)  # Store the rectangle reference
#         plt.draw()  # Update the plot
        
#         # Deactivate the selector
#         self.deactivate_selector()

#     def activate_selector(self, event):
#         """This function activates the RectangleSelector when called."""
#         if self.rect_selector is None:  # Create it only once
#             self.rect_selector = RectangleSelector(
#                 self.ax, 
#                 onselect=self.on_select, 
#                 interactive=True  # Make the rectangle draggable and resizable
#             )
#             print(f"RectangleSelector activated on {self.ax.get_title()}.")
#         else:
#             self.rect_selector.set_active(True)  # Re-activate if already created

#     def deactivate_selector(self):
#         """Deactivate the rectangle selector."""
#         if self.rect_selector is not None:
#             self.rect_selector.set_active(False)  # Deactivate the selector
#             print(f"RectangleSelector deactivated on {self.ax.get_title()}.")

#     def clear_rectangles(self):
#         """Remove all created rectangles from the axis."""
#         for rect in self.rectangles:
#             rect.remove()  # Remove the rectangle from the plot
#         self.rectangles.clear()  # Clear the list of rectangles
#         plt.draw()  # Update the plot
#         print(f"All rectangles removed from {self.ax.get_title()}.")

# # Create a figure with two subplots
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# # Plot some data on the first graph (ax1)
# x = [1, 2, 3, 4, 5]
# y1 = [2, 3, 4, 5, 6]
# ax1.plot(x, y1)
# ax1.set_title('Graph 1')

# # Plot some data on the second graph (ax2)
# y2 = [1, 4, 2, 5, 3]
# ax2.plot(x, y2)
# ax2.set_title('Graph 2')

# # Instantiate DraggableRectangle for each graph
# draggable_rect1 = DraggableRectangle(ax1)
# draggable_rect2 = DraggableRectangle(ax2)

# # Create buttons for each graph
# ax_button1 = plt.axes([0.1, 0.05, 0.2, 0.075])  # Button position for the first graph
# button1 = Button(ax_button1, 'Activate Graph 1')
# button1.on_clicked(draggable_rect1.activate_selector)

# ax_button2 = plt.axes([0.4, 0.05, 0.2, 0.075])  # Button position for the second graph
# button2 = Button(ax_button2, 'Activate Graph 2')
# button2.on_clicked(draggable_rect2.activate_selector)

# # Create a deactivate button for both graphs
# ax_deactivate = plt.axes([0.7, 0.05, 0.2, 0.075])  # Button position for deactivating both
# deactivate_button = Button(ax_deactivate, 'Deactivate Both Rectangles')

# def deactivate_both_rectangles(event):
#     # Call the clear method for both rectangles
#     draggable_rect1.clear_rectangles()
#     draggable_rect2.clear_rectangles()

#     # Reset the state of both rectangle selectors
#     draggable_rect1.deactivate_selector()
#     draggable_rect2.deactivate_selector()

#     # Re-enable the activate buttons
#     button1.label.set_text('Activate Graph 1')
#     button2.label.set_text('Activate Graph 2')

# deactivate_button.on_clicked(deactivate_both_rectangles)

# plt.tight_layout()
# plt.show()






