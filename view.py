import tkinter as tk

from constants import ViewFormat

class View:
  def __init__(self, lbl_left_click_handler, lbl_right_click_handler,
               notes_updated_handler, view_toggle_handler):
    #root = tk.Tk()
    #window = tk.Toplevel()
    self.window = tk.Tk()
    self.window.title("snote")
    
    #window.overrideredirect(True)
    #window.wm_attributes('-type','splash')
    #window.lift()
    self.window.wm_attributes("-topmost", True)
    #window.wm_attributes("-disabled", True)
    #window.wm_attributes("-transparentcolor", "white")

    # https://stackoverflow.com/questions/28419763/expand-text-widget-to-fill-the-entire-parent-frame-in-tkinter
    self.window.grid_columnconfigure(0, weight=1)
    self.window.grid_rowconfigure(0, weight=1)

    self.lbl = tk.Label(self.window, text="Loading...")
    self.lbl.grid(column=0, row=1, sticky=tk.E+tk.W)
    self.lbl.bind("<Button-1>", lbl_left_click_handler)
    self.lbl.bind("<Button-3>", lbl_right_click_handler)

    # hack from https://stackoverflow.com/questions/46284901/how-do-i-resize-buttons-in-pixels-tkinter/46286221#46286221
    self.pixel = tk.PhotoImage(width=1, height=1)
    self.view_toggle_button = tk.Button(self.window, image=self.pixel, height=16, width=16,
      command = view_toggle_handler)
    self.view_toggle_button.grid(column=1, row=1)

    self.notes_scroll = tk.Scrollbar(self.window)
    self.notes_text = tk.Text(self.window, height=4, width=50)
    self.notes_scroll.config(command=self.notes_text.yview)
    self.notes_text.config(yscrollcommand=self.notes_scroll.set)
    self.notes_text.grid(column=0,row=0, sticky="ewns")
    self.notes_scroll.grid(column=1,row=0, sticky="ns")
    self.notes_text.bind("<KeyRelease>", notes_updated_handler)

    self.build_scroll = tk.Scrollbar(self.window)
    self.build_text = tk.Text(self.window, height=4, width=50)
    self.build_scroll.config(command=self.build_text.yview)
    self.build_text.config(yscrollcommand=self.notes_scroll.set)
    self.build_text.grid(column=0,row=0, sticky="ewns")
    self.build_scroll.grid(column=1,row=0, sticky="ns")
    self.build_text.tag_configure("bold", font="bold")

  def SetViewFormat(self, format):
    for item in self.window.grid_slaves():
      item.grid_remove()
    if format == ViewFormat.TAB:
      elements = [self.lbl]
      height = 18
      width = 18
    elif format == ViewFormat.LABEL_ONLY:
      elements = [self.lbl]
      height = 18
      width = 300
    elif format == ViewFormat.NOTES_VIEW:
      elements = [self.lbl, self.view_toggle_button, self.notes_scroll, self.notes_text]
      height = 300
      width = 300
    elif format == ViewFormat.BUILD_VIEW:
      elements = [self.lbl, self.view_toggle_button, self.build_scroll, self.build_text]
      height = 300
      width = 300
    else:
      raise ValueError("unknown ViewFormat")
    for item in elements:
      item.grid()
    left = 5
    top = 718 - height
    self.window.geometry('{}x{}+{}+{}'.format(width, height, left, top))

  def Run(self):
    self.window.mainloop()

  def GetVillainNotes(self):
    return self.notes_text.get(1.0, tk.END)

  def SetLabelText(self, text):
    self.lbl.configure(text=text)

  def SetNotesText(self, text):
    self.notes_text.delete(1.0, tk.END)
    self.notes_text.insert(tk.END, text)
    self.notes_text.configure(state=tk.NORMAL)

  def SetBuildText(self, past='', future=''):
    # include at most 4 lines of past
    past = '\n'.join(past.split('\n')[-4:])
    # set text
    self.build_text.configure(state=tk.NORMAL)
    self.build_text.delete(1.0, tk.END)
    self.build_text.insert(tk.END, past)
    if past:
      self.build_text.insert(tk.END, '\n')
    self.build_text.insert(tk.END, future, 'bold')
    self.build_text.configure(state=tk.DISABLED)

  # Repeatedly call func every delay_ms.
  def AddTask(self, func, delay_ms):
    def f():
      func()
      self.window.after(delay_ms, f)
    f()
