import tkinter as tk
from tkinter import messagebox
import mysql.connector as sqltor

def connect():

    def try_connect():
        try:
            conn = sqltor.connect(host = tb_host.get(), user = tb_user.get(), passwd = tb_password.get(), database = tb_database.get())
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Rooms ( roomid int AUTO_INCREMENT PRIMARY KEY, name varchar(30), guest varchar(50) );" )
            conn.commit()
            cur.close()
            
            conn_win.destroy()
            init_win(conn)
        except:
            messagebox.showwarning("Error", "The entered details are not correct. Please enter correct details to continue")
    
    try:
        conn = sqltor.connect(host = "localhost", user = "root", passwd = "mysql@123", database = "project")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Rooms ( roomid int AUTO_INCREMENT PRIMARY KEY, name varchar(30), guest varchar(50) );" )
        conn.commit()
        cur.close()
    except:
        conn_win = tk.Tk()
        conn_win.title("Connecting to database")

        lbl_details = tk.Label(conn_win, text = "Please enter the details of the SQL database to connect to it").grid(row = 0, column = 0, columnspan = 2)
        
        lbl_host = tk.Label(conn_win, text = "Host:").grid(row = 1, column = 0)
        lbl_user = tk.Label(conn_win, text = "User:").grid(row = 2, column = 0)
        lbl_password = tk.Label(conn_win, text = "Password:").grid(row = 3, column = 0)
        lbl_database = tk.Label(conn_win, text = "Database:").grid(row = 4, column = 0)

        tb_host = tk.Entry(conn_win)
        tb_user = tk.Entry(conn_win)
        tb_password = tk.Entry(conn_win, show = '*')
        tb_database = tk.Entry(conn_win)

        tb_host.grid(row = 1, column = 1)
        tb_user.grid(row = 2, column = 1)
        tb_password.grid(row = 3, column = 1)
        tb_database.grid(row = 4, column = 1)

        btn_confirm = tk.Button(conn_win, text = "Confirm", command = try_connect)
        btn_confirm.grid(row = 5, column = 0, columnspan = 2)

        conn_win.mainloop()
    
    init_win(conn)
    return
  
def init_win(conn):
    win = tk.Tk()
    win.title("Hotel management")
    win.geometry('1000x500')

    frm_tabs = tk.Frame(win, width = 50, height = 100)
    frm_tabs.place(relx = 0.02, rely = 0.5, anchor = 'w')

    frm_content = tk.Frame(win, width = 700, height = 500)
    frm_content.place(relx = 0.5, rely = 0.5, anchor = 'center')

    btn_rooms = tk.Button(frm_tabs, text = "Manage rooms", command = lambda: display_tab(conn, frm_content, "rooms"), width = 15)
    btn_rooms.grid(row = 0, column = 0, pady = 2)
    
    btn_assign = tk.Button(frm_tabs, text = "Checkin/Checkout", command = lambda: display_tab(conn, frm_content, "guests"), width = 15)
    btn_assign.grid(row = 1, column = 0, pady = 2)

    win.mainloop()

def display_tab(conn, frm_content, tab):
    for widget in frm_content.winfo_children():
        widget.destroy()
    
    if tab == "rooms":
        lbl_add = tk.Label(frm_content, text = "Add a new room")
        lbl_add.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        lbl_room_add = tk.Label(frm_content, text = "Enter name of room : ")
        lbl_room_add.grid(row = 1, column = 0, sticky = 'e', padx = 1, pady = 5)

        tb_room_add = tk.Entry(frm_content)
        tb_room_add.grid(row = 1, column = 1, sticky = 'w', padx = 1, pady = 5)

        btn_add = tk.Button(frm_content, text = "Add room", command = lambda: add_room(conn, tb_room_add.get(), frm_content) )
        btn_add.grid(row = 2, column = 0, columnspan = 2, pady = 10)

        tk.Label(frm_content).grid(row = 3, column = 0, pady = 5)

        lbl_delete = tk.Label(frm_content, text = "Delete an existing room")
        lbl_delete.grid(row = 4, column = 0, columnspan = 2, pady = 20)

        lbl_room_del = tk.Label(frm_content, text = "Choose room to delete:")
        lbl_room_del.grid(row = 5, column = 0, sticky = 'e', padx = 1, pady = 5)

        room_list = get_rooms(conn)
        if room_list != []:
            del_room = tk.StringVar()
            optmen_rem_room = tk.OptionMenu(frm_content, del_room, *room_list)
            optmen_rem_room.grid(row = 5, column = 1)

        btn_del = tk.Button(frm_content, text = "Delete room", command = lambda: delete_room(conn, del_room.get(), frm_content) )
        btn_del.grid(row = 6, column = 0, columnspan = 2, pady = 10)

    if tab == "guests":
        lbl_assign = tk.Label(frm_content, text = "Check in a guest")
        lbl_assign.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        lbl_checkin_room = tk.Label(frm_content, text = "Choose room to check in:")
        lbl_checkin_room.grid(row = 1, column = 0, sticky = 'e', padx = 1, pady = 5)

        room_list = get_rooms(conn, True)
        if room_list != []:
            checkin_room = tk.StringVar()
            optmen_checkin_room = tk.OptionMenu(frm_content, checkin_room, *room_list)
            optmen_checkin_room.grid(row = 1, column = 1)

        lbl_guest_name = tk.Label(frm_content, text = "Enter name of guest:")
        lbl_guest_name.grid(row = 2, column = 0, sticky = 'e', padx = 1, pady = 5)

        tb_guest_name = tk.Entry(frm_content)
        tb_guest_name.grid(row = 2, column = 1, sticky = 'w', padx = 1, pady = 5)

        btn_checkin = tk.Button(frm_content, text = "Check in", command = lambda: checkin(conn, checkin_room.get(), tb_guest_name.get(), frm_content) )
        btn_checkin.grid(row = 3, column = 0, columnspan = 2, pady = 10)

        tk.Label(frm_content).grid(row = 4, column = 0, pady = 5)

        lbl_checkout = tk.Label(frm_content, text = "Check out a guest")
        lbl_checkout.grid(row = 5, column = 0, columnspan = 2, pady = 20)

        lbl_checkout_room = tk.Label(frm_content, text = "Choose room to check out:")
        lbl_checkout_room.grid(row = 6, column = 0, sticky = 'e', padx = 1, pady = 5)

        room_guest_list = get_rooms_guests(conn)
        if room_guest_list != []:
            checkout_room = tk.StringVar()
            optmen_checkout_room = tk.OptionMenu(frm_content, checkout_room, *room_guest_list)
            optmen_checkout_room.grid(row = 6, column = 1)

        btn_checkout = tk.Button(frm_content, text = "Check out", command = lambda: checkout(conn, checkout_room.get().split()[0], frm_content) )
        btn_checkout.grid(row = 7, column = 0, columnspan = 2, pady = 10)
        
def get_rooms(conn, available = False):
    cur = conn.cursor()
    
    if available:
        cur.execute("SELECT name FROM Rooms WHERE guest IS NULL")
    else:
        cur.execute("SELECT name FROM Rooms;")
    
    room_list = cur.fetchall()
    cur.close()
    
    if room_list == []:
        return( [] )
    else:
        return( list(zip(*room_list))[0] )

def get_rooms_guests(conn):
    cur = conn.cursor()
    cur.execute("SELECT name, guest FROM Rooms WHERE guest IS NOT NULL;")
    room_list = cur.fetchall()
    cur.close()
    if room_list == []:
        return([])
    else:
        room_guest_list = []
        for tup in room_list:
            room_guest_list.append(tup[0] + ' - ' + tup[1])
        return( room_guest_list )

def add_room(conn, room, frm_content):
    room_list = get_rooms(conn)
    if room in room_list:
        messagebox.showwarning("Room already exists", "Two rooms cannot have the same name")
    else:
        cur = conn.cursor()
        cur.execute("INSERT INTO Rooms (name, guest) VALUES (%s, NULL);" , (room,) )
        conn.commit()
        cur.close()
        display_tab(conn, frm_content, "rooms")

def delete_room(conn, room, frm_content):
    cur = conn.cursor()
    cur.execute("DELETE FROM Rooms WHERE name = %s ;" , (room,) )
    conn.commit()
    cur.close()
    display_tab(conn, frm_content, "rooms")

def checkin(conn, room, guest, frm_content):
    cur = conn.cursor()
    cur.execute("UPDATE Rooms SET guest = %s WHERE name = %s ;", (guest, room) )
    conn.commit()
    cur.close()
    display_tab(conn, frm_content, "guests")

def checkout(conn, room, frm_content):
    cur = conn.cursor()
    cur.execute("UPDATE Rooms SET guest = NULL WHERE name = %s ;", (room,) )
    conn.commit()
    cur.close()
    display_tab(conn, frm_content, "guests")
    
if __name__ == "__main__":
    connect()
