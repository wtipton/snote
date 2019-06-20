import tkinter as tk

from constants import ViewFormat

class View:
  def __init__(self, lbl_left_click_handler, lbl_right_click_handler, notes_updated_handler):
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
    self.window.grid_rowconfigure(1, weight=1)

    self.lbl = tk.Label(self.window, text="Loading...")
    self.lbl.grid(column=0, row=0, columnspan=2, sticky=tk.E+tk.W)
    self.lbl.bind("<Button-1>", lbl_left_click_handler)
    self.lbl.bind("<Button-3>", lbl_right_click_handler)

    self.S = tk.Scrollbar(self.window)
    self.T = tk.Text(self.window, height=4, width=50)
    self.S.config(command=self.T.yview)
    self.T.config(yscrollcommand=self.S.set)
    self.T.grid(column=0,row=1, sticky="ewns")
    self.S.grid(column=1,row=1, sticky="ns")
    self.T.bind("<KeyRelease>", notes_updated_handler)

  def SetViewFormat(self, format):
    if format == ViewFormat.TAB:
      height = 18
      width = 18
    elif format == ViewFormat.LABEL_ONLY:
      height = 18
      width = 300
    else:
      height = 300
      width = 300
    self.window.geometry(str(width)+"x"+str(height)+"+5+700")

  def Run(self):
    self.window.mainloop()

  def GetVillainNotes(self):
    return self.T.get(1.0, tk.END)

  def SetLabelText(self, text):
    self.lbl.configure(text=text)

  def SetNotesText(self, text):
    self.T.delete(1.0, tk.END)
    self.T.insert(tk.END, text)
    self.T.configure(state=tk.NORMAL)     

  def AddTask(self, func, delay_ms):
    def f():
      func()
      self.window.after(delay_ms, f)
    f()
