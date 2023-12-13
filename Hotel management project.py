import tkinter as tk
from tkinter import messagebox
import mysql.connector as sqltor
from datetime import date

def connect():

    def try_connect():
        try:
            conn = sqltor.connect(host = tb_host.get(), user = tb_user.get(), passwd = tb_password.get(), database = tb_database.get())
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Rooms ( roomid int AUTO_INCREMENT PRIMARY KEY, name varchar(30), price int, guest varchar(50), checkin_date date );" )
            conn.commit()
            cur.close()
            
            conn_win.destroy()
            init_win(conn)
        except:
            messagebox.showwarning("Error", "The entered details are not correct. Please enter correct details to continue")
    
    try:
        conn = sqltor.connect(host = "localhost", user = "root", passwd = "mysql@123", database = "project")
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Rooms ( roomid int AUTO_INCREMENT PRIMARY KEY, name varchar(30), price int, guest varchar(50), checkin_date date );" )
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

    btn_tags = tk.Button(frm_tabs, text = "Manage tags", command = lambda: display_tab(conn, frm_content, "tags"), width = 15)
    btn_tags.grid(row = 3, column = 0, pady = 2)

    btn_asn_rem = tk.Button(frm_tabs, text = "Assign/Remove tags", command = lambda: display_tab(conn, frm_content, "room tags"), width = 15)
    btn_asn_rem.grid(row = 4, column = 0, pady = 2)

    btn_search = tk.Button(frm_tabs, text = "Search", command = lambda: display_tab(conn, frm_content, "search"), width = 15)
    btn_search.grid(row = 5, column = 0, pady = 2)

    win.mainloop()

def display_tab(conn, frm_content, tab, room_data = None):
    for widget in frm_content.winfo_children():
        widget.destroy()
    
    if tab == "rooms":
        del_room = tk.StringVar()
        
        lbl_add = tk.Label(frm_content, text = "Add a new room")
        lbl_add.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        lbl_room_add = tk.Label(frm_content, text = "Enter name of room : ")
        lbl_room_add.grid(row = 1, column = 0, sticky = 'e', padx = 1, pady = 5)

        tb_room_add = tk.Entry(frm_content)
        tb_room_add.grid(row = 1, column = 1, sticky = 'w', padx = 1, pady = 5)

        lbl_room_price = tk.Label(frm_content, text = "Enter price per night of the room : ")
        lbl_room_price.grid(row = 2, column = 0, sticky = 'e', padx = 1, pady = 5)

        tb_room_price = tk.Entry(frm_content)
        tb_room_price.grid(row = 2, column = 1, sticky = 'w', padx = 1, pady = 5)

        btn_add = tk.Button(frm_content, text = "Add room", command = lambda: add_room(conn, tb_room_add.get(), tb_room_price.get(), lambda: display_tab(conn, frm_content, 'rooms')) )
        btn_add.grid(row = 3, column = 0, columnspan = 2, pady = 10)

        tk.Label(frm_content).grid(row = 4, column = 0, pady = 5)

        lbl_delete = tk.Label(frm_content, text = "Delete an existing room")
        lbl_delete.grid(row = 5, column = 0, columnspan = 2, pady = 20)

        lbl_room_del = tk.Label(frm_content, text = "Choose room to delete:")
        lbl_room_del.grid(row = 6, column = 0, sticky = 'e', padx = 1, pady = 5)

        room_list = get_rooms(conn)
        if room_list != []:
            optmen_rem_room = tk.OptionMenu(frm_content, del_room, *room_list)
            optmen_rem_room.grid(row = 6, column = 1)

        btn_del = tk.Button(frm_content, text = "Delete room", command = lambda: delete_room(conn, del_room.get(), lambda: display_tab(conn, frm_content, 'rooms')) )
        btn_del.grid(row = 7, column = 0, columnspan = 2, pady = 10)

    elif tab == "guests":
        checkin_room = tk.StringVar()
        checkout_room = tk.StringVar()
        checkout_room.set(chr(0)+' '+chr(0))
        
        lbl_assign = tk.Label(frm_content, text = "Check in a guest")
        lbl_assign.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        lbl_checkin_room = tk.Label(frm_content, text = "Choose room to check in:")
        lbl_checkin_room.grid(row = 1, column = 0, sticky = 'e', padx = 1, pady = 5)

        room_list = get_rooms(conn, True)
        if room_list != []:
            optmen_checkin_room = tk.OptionMenu(frm_content, checkin_room, *room_list)
            optmen_checkin_room.grid(row = 1, column = 1)

        lbl_guest_name = tk.Label(frm_content, text = "Enter name of guest:")
        lbl_guest_name.grid(row = 2, column = 0, sticky = 'e', padx = 1, pady = 5)

        tb_guest_name = tk.Entry(frm_content)
        tb_guest_name.grid(row = 2, column = 1, sticky = 'w', padx = 1, pady = 5)

        btn_checkin = tk.Button(frm_content, text = "Check in", command = lambda: checkin(conn, checkin_room.get(), tb_guest_name.get(), lambda: display_tab(conn, frm_content, 'guests')) )
        btn_checkin.grid(row = 3, column = 0, columnspan = 2, pady = 10)

        tk.Label(frm_content).grid(row = 4, column = 0, pady = 5)

        lbl_checkout = tk.Label(frm_content, text = "Check out a guest")
        lbl_checkout.grid(row = 5, column = 0, columnspan = 2, pady = 20)

        lbl_checkout_room = tk.Label(frm_content, text = "Choose room to check out:")
        lbl_checkout_room.grid(row = 6, column = 0, sticky = 'e', padx = 1, pady = 5)

        room_guest_list = get_rooms_guests(conn)
        if room_guest_list != []:
            optmen_checkout_room = tk.OptionMenu(frm_content, checkout_room, *room_guest_list)
            optmen_checkout_room.grid(row = 6, column = 1)

        btn_checkout = tk.Button(frm_content, text = "Check out", command = lambda: checkout(conn, checkout_room.get().split(' ')[0], lambda: display_tab(conn, frm_content, 'guests')) )
        btn_checkout.grid(row = 7, column = 0, columnspan = 2, pady = 10)

    elif tab == "tags":
        del_tag = tk.StringVar()

        lbl_new_tag = tk.Label(frm_content, text = "Create a new tag")
        lbl_new_tag.grid(row = 0, column = 0, columnspan = 2, pady = 10)

        lbl_create_tag = tk.Label(frm_content, text = "Enter name of tag:")
        lbl_create_tag.grid(row = 1, column = 0, sticky = 'e', padx = 1, pady = 2.5)

        tb_create_tag = tk.Entry(frm_content)
        tb_create_tag.grid(row = 1, column = 1, sticky = 'w', padx = 1, pady = 2.5)

        btn_create_tag = tk.Button(frm_content, text = "Create Tag", command = lambda: add_tag(conn, tb_create_tag.get(), lambda: display_tab(conn, frm_content, 'tags')) )
        btn_create_tag.grid(row = 2, column = 0, columnspan = 2, pady = 5)

        tk.Label(frm_content).grid(row = 3, column = 0, pady = 2.5)

        lbl_delete = tk.Label(frm_content, text = "Delete an existing tag")
        lbl_delete.grid(row = 4, column = 0, columnspan = 2, pady = 10)

        lbl_del_tag = tk.Label(frm_content, text = "Choose tag to delete:")
        lbl_del_tag.grid(row = 5, column = 0, sticky = 'e', padx = 1, pady = 2.5)

        tags = get_tags(conn)
        if tags != []:
            optmen_del_room = tk.OptionMenu(frm_content, del_tag, *tags )
            optmen_del_room.grid(row = 5, column = 1)

        btn_del_tag = tk.Button(frm_content, text = "Delete Tag", command = lambda: delete_tag(conn, del_tag.get(), lambda: display_tab(conn, frm_content, 'tags')) )
        btn_del_tag.grid(row = 6, column = 0, columnspan = 2, pady = 5)

        tk.Label(frm_content).grid(row = 7, column = 0, pady = 2.5)

    elif tab == "room tags":
        assign_room = tk.StringVar()
        assign_tag_name = tk.StringVar()
        remove_tag_name = tk.StringVar()
        remove_room_name = tk.StringVar()
        
        lbl_assign = tk.Label(frm_content, text = "Assign tags to rooms")
        lbl_assign.grid(row = 0, column = 0, columnspan = 2, pady = 10)

        lbl_assign_room = tk.Label(frm_content, text = "Choose room to assign tag to:")
        lbl_assign_room.grid(row = 1, column = 0, sticky = 'e', padx = 1, pady = 2.5)

        room_list = get_rooms(conn)
        if room_list != []:
            optmen_assign_room = tk.OptionMenu(frm_content, assign_room, *room_list)
            optmen_assign_room.grid(row = 1, column = 1)

        lbl_assign_tag = tk.Label(frm_content, text = "Choose tag to assign:")
        lbl_assign_tag.grid(row = 2, column = 0, sticky = 'e', padx = 1, pady = 2.5)

        tag_list = get_tags(conn)
        if tag_list != []:
            optmen_assign_tag = tk.OptionMenu(frm_content, assign_tag_name, *tag_list)
            optmen_assign_tag.grid(row = 2, column = 1)

        btn_assign = tk.Button(frm_content, text = "Assign tag", command = lambda: assign_tag(conn, assign_room.get(), assign_tag_name.get(), lambda: display_tab(conn, frm_content, 'room tags') ))
        btn_assign.grid(row = 3, column = 0, columnspan = 2, pady = 5)

        tk.Label(frm_content).grid(row = 4, column = 0, pady = 2.5)

        lbl_assign = tk.Label(frm_content, text = "Remove tags from rooms")
        lbl_assign.grid(row = 5, column = 0, columnspan = 2, pady = 10)

        lbl_assign_room = tk.Label(frm_content, text = "Choose room to remove tag from:")
        lbl_assign_room.grid(row = 6, column = 0, sticky = 'e', padx = 1, pady = 2.5)

        def update_rem_tag_list(conn, frm_content, room):
            frm_content.winfo_children()[12].destroy()
            remove_tag_name.set("")
            
            tag_list = get_tags(conn, room)
            if tag_list != []:
                optmen_remove_tag = tk.OptionMenu(frm_content, remove_tag_name, *tag_list)
                optmen_remove_tag.grid(row = 7, column = 1)
            else:
                optmen_remove_tag = tk.Label(frm_content)
                optmen_remove_tag.grid(row = 7, column = 1)

        room_list = get_rooms(conn)
        if room_list != []:
            optmen_remove_room = tk.OptionMenu(frm_content, remove_room_name, *room_list, command = lambda event: update_rem_tag_list(conn, frm_content, remove_room_name.get()))
            optmen_remove_room.grid(row = 6, column = 1)

        lbl_remove_tag = tk.Label(frm_content, text = "Choose tag to remove:")
        lbl_remove_tag.grid(row = 7, column = 0, sticky = 'e', padx = 1, pady = 2.5)

        btn_remove = tk.Button(frm_content, text = "Remove tag", command = lambda: remove_tag(conn, remove_room_name.get(), remove_tag_name.get(), lambda: display_tab(conn, frm_content, 'room tags') ))
        btn_remove.grid(row = 8, column = 0, columnspan = 2, pady = 5)
        
        optmen_remove_tag = tk.Label(frm_content)
        optmen_remove_tag.grid(row = 7, column = 1)

    elif tab == "search":
        lbl_heading = tk.Label(frm_content, text = "Search", font = ('Helvetica', 15, 'bold'))
        lbl_heading.grid(row = 0, column = 0, columnspan = 4, pady = 10)
        
        lbl_room_name = tk.Label(frm_content, text = "Name of the room:")
        lbl_room_name.grid(row = 1, column = 0, columnspan = 2, sticky = 'e', padx = 1, pady = 2.5)

        tb_room_name = tk.Entry(frm_content)
        tb_room_name.grid(row = 1, column = 2, columnspan = 2, sticky = 'w', padx = 1, pady = 2.5)

        applied_filters = []
        lbl_filters = tk.Label(frm_content, text = "Applied Filters : ")
        lbl_filters.grid(row = 2, column = 0, columnspan = 4, pady = 5, sticky = 'w')

        lbl_new_filter = tk.Label(frm_content, text = "Add new filter:")
        lbl_new_filter.grid(row = 3, column = 0, sticky = 'e', padx = 1, pady = 2.5)
        
        new_filter_name = tk.StringVar()
        tag_list = get_tags(conn)
        if tag_list != []:
            optmen_new_filter = tk.OptionMenu(frm_content, new_filter_name, *tag_list)
            optmen_new_filter.grid(row = 3, column = 1)

        btn_add_filter = tk.Button(frm_content, text = "Add filter")
        btn_add_filter.grid(row = 4, column = 0, columnspan = 2, pady = 4)

        lbl_new_filter = tk.Label(frm_content, text = "Remove filter:")
        lbl_new_filter.grid(row = 3, column = 2, sticky = 'e', padx = 1, pady = 2.5)
        
        rem_filter_name = tk.StringVar()
        optmen_rem_filter = tk.OptionMenu(frm_content, rem_filter_name, '')
        optmen_rem_filter.grid(row = 3, column = 3)

        btn_add_filter.config(command = lambda: add_filter(new_filter_name.get(), applied_filters, lbl_filters, optmen_rem_filter, rem_filter_name) )

        btn_rem_filter = tk.Button(frm_content, text = "Remove filter", command = lambda: rem_filter(rem_filter_name.get(), applied_filters, lbl_filters, optmen_rem_filter, rem_filter_name) )
        btn_rem_filter.grid(row = 4, column = 2, columnspan = 2, pady = 4)

        available = tk.IntVar()
        available.set(0)
        cb_availability = tk.Checkbutton(frm_content, text = "Available", variable = available, onvalue = 1, offvalue = 0)
        cb_availability.grid(row = 5, column = 0, columnspan = 4, pady = 2.5)

        btn_search = tk.Button(frm_content, text = "Search")
        btn_search.grid(row = 6, column = 0, columnspan = 4, pady = 5)

        frm_results = tk.Frame(frm_content)
        frm_results.grid(row = 7, column = 0, columnspan = 4, pady = 3)
        scroll_lb = tk.Scrollbar(frm_results, orient = "vertical")
        lb_results = tk.Listbox(frm_results, width = 100, yscrollcommand = scroll_lb.set, selectmode = "single")
        scroll_lb.config(command = lb_results.yview)
        scroll_lb.pack(side = "right", fill = "y")
        lb_results.pack()

        btn_search.config(command = lambda: search(conn, tb_room_name.get(), applied_filters, available.get(), lb_results))
        
        btn_select = tk.Button(frm_content, text = "Select", command = lambda: search_select(conn, lb_results.get("anchor"), frm_content))
        btn_select.grid(row = 9, column = 0, columnspan = 4, pady = 5)

    elif tab == "specific room":
        lbl_heading = tk.Label(frm_content, text = "Room : " + room_data[1], font = ('Helvetica', 15, 'bold'))
        lbl_heading.grid(row = 0, column = 0, columnspan = 4, pady = 5)

        lbl_price = tk.Label(frm_content, text = "Price per night : " + str(room_data[2]), font = ('Helvetica', 10))
        lbl_price.grid(row = 1, column = 0, columnspan = 4, sticky = 'w', pady = 2.5)

        tags_list = get_tags(conn, room_data[1])
        lbl_tags = tk.Label(frm_content, text = "Tags : " + ', '.join(tags_list), font = ('Helvetica', 10))
        lbl_tags.grid(row = 2, column = 0, columnspan = 4, sticky = 'w', pady = 2.5)

        lbl_guest = tk.Label(frm_content, text = "Guest : " + str(room_data[3]), font = ('Helvetica', 10))
        lbl_guest.grid(row = 3, column = 0, columnspan = 4, sticky = 'w', pady = 2.5)

        if room_data[3] == None:
            lbl_checkin = tk.Label(frm_content, text = "Check in guest")
            lbl_checkin.grid(row = 4, column = 0, columnspan = 4, pady = 7.5)

            lbl_checkin_guest = tk.Label(frm_content, text = "Enter name of guest:")
            lbl_checkin_guest.grid(row = 5, column = 0, columnspan = 2, sticky = 'e', padx = 1, pady = 1)

            tb_checkin_guest = tk.Entry(frm_content)
            tb_checkin_guest.grid(row = 5, column = 2, columnspan = 2, sticky = 'w', padx = 1, pady = 1)

            btn_checkin = tk.Button(frm_content, text = "Check in", command = lambda: checkin(conn, room_data[1], tb_checkin_guest.get(), lambda: search_select(conn, room_data[1], frm_content)) )
            btn_checkin.grid(row = 6, column = 0, columnspan = 4, pady = 2.5)
            
        else:
            btn_checkout = tk.Button(frm_content, text = "Check out guest", command = lambda: checkout(conn, room_data[1], lambda: search_select(conn, room_data[1], frm_content)) )
            btn_checkout.grid(row = 4, column = 0, columnspan = 4, pady = 5)

        tk.Label(frm_content).grid(row = 7, column = 0, columnspan = 4, pady = 1)

        lbl_assign = tk.Label(frm_content, text = "Add tag to room")
        lbl_assign.grid(row = 8, column = 0, columnspan = 2, pady = 7.5)

        lbl_assign_tag = tk.Label(frm_content, text = "Choose tag to assign:")
        lbl_assign_tag.grid(row = 9, column = 0, sticky = 'e', padx = 1, pady = 1)

        all_tag_list = get_tags(conn)
        assign_tag_name = tk.StringVar()
        if all_tag_list != []:
            optmen_assign_tag = tk.OptionMenu(frm_content, assign_tag_name, *all_tag_list)
            optmen_assign_tag.grid(row = 9, column = 1, padx = 1)

        btn_assign = tk.Button(frm_content, text = "Add tag", command = lambda: assign_tag(conn, room_data[1], assign_tag_name.get(), lambda: search_select(conn, room_data[1], frm_content) ))
        btn_assign.grid(row = 10, column = 0, columnspan = 2, pady = 2.5)

        lbl_remove = tk.Label(frm_content, text = "Remove tag from room")
        lbl_remove.grid(row = 8, column = 2, columnspan = 2, pady = 7.5)

        lbl_remove_tag = tk.Label(frm_content, text = "Choose tag to remove:")
        lbl_remove_tag.grid(row = 9, column = 2, sticky = 'e', padx = 1, pady = 1)

        remove_tag_name = tk.StringVar()
        if tags_list != []:
            optmen_remove_tag = tk.OptionMenu(frm_content, remove_tag_name, *tags_list)
            optmen_remove_tag.grid(row = 9, column = 3, padx = 1)

        btn_remove_tag = tk.Button(frm_content, text = "Remove tag", command = lambda: remove_tag(conn, room_data[1], remove_tag_name.get(), lambda: search_select(conn, room_data[1], frm_content) ))
        btn_remove_tag.grid(row = 10, column = 2, columnspan = 2, pady = 2.5)

        tk.Label(frm_content).grid(row = 11, column = 0, columnspan = 4, pady = 2)

        lbl_edit_name = tk.Label(frm_content, text = "Change name of the room")
        lbl_edit_name.grid(row = 12, column = 0, columnspan = 2, pady = 7.5)

        lbl_new_name = tk.Label(frm_content, text = "Enter new name:")
        lbl_new_name.grid(row = 13, column = 0, sticky = 'e', padx = 1, pady = 1)

        tb_new_name = tk.Entry(frm_content)
        tb_new_name.grid(row = 13, column = 1, sticky = 'w', padx = 1, pady = 1)

        btn_change_name = tk.Button(frm_content, text = "Change name", command = lambda: change_name(conn, room_data[0], room_data[1], tb_new_name.get(), lambda: search_select(conn, tb_new_name.get(), frm_content)) )
        btn_change_name.grid(row = 14, column = 0, columnspan = 2, pady = 2.5)
        
        lbl_edit_price = tk.Label(frm_content, text = "Change price of the room")
        lbl_edit_price.grid(row = 12, column = 2, columnspan = 2, pady = 7.5)

        lbl_new_price = tk.Label(frm_content, text = "Enter new price:")
        lbl_new_price.grid(row = 13, column = 2, sticky = 'e', padx = 1, pady = 1)

        tb_new_price = tk.Entry(frm_content)
        tb_new_price.grid(row = 13, column = 3, sticky = 'w', padx = 1, pady = 1)

        btn_change_price = tk.Button(frm_content, text = "Change price", command = lambda: change_price(conn, room_data[0], tb_new_price.get(), lambda: search_select(conn, room_data[1], frm_content)))
        btn_change_price.grid(row = 14, column = 2, columnspan = 2, pady = 2.5)

        btn_delete_room = tk.Button(frm_content, text = "Delete Room", command = lambda: delete_room(conn, room_data[1], lambda: display_tab(conn, frm_content, tab = 'search')) )
        btn_delete_room.grid(row = 15, column = 0, columnspan = 4, sticky = 'e', pady = 20)
        
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

def get_tags(conn, room = None):
    cur = conn.cursor()
    cur.execute("SELECT * from Rooms WHERE name = NULL;")
    cur.fetchall()
    columns = cur.column_names
    if len(columns) <= 5:
        return([])
    else:
        tags = columns[5::]
        
    if room == None:
        return(tags)
    else:
        applied_tags = []
        cur.execute("SELECT * FROM Rooms WHERE name = %s",(room,))
        tag_values = cur.fetchall()[0][5::]
        for i in range(len(tag_values)):
            if tag_values[i] == 1:
                applied_tags.append(tags[i])

        return(applied_tags)
            

def add_room(conn, room, price, refresh):
    room_list = get_rooms(conn)
    if room == '':
        messagebox.showwarning("Room name cannot be empty", "Please enter name of the room")
    elif room in room_list:
        messagebox.showwarning("Room already exists", "Two rooms cannot have the same name")
    elif not price.isdigit():
        messagebox.showwarning("Price should be a number", "Price should be a positive whole number")
    else:
        cur = conn.cursor()
        cur.execute("INSERT INTO Rooms (name, price, guest) VALUES (%s, %s, NULL);" , (room, price))
        conn.commit()
        cur.close()
        refresh()

def delete_room(conn, room, refresh):
    if room == '':
        messagebox.showwarning("Room not selected", "Please select a room to delete")
    else:
        cur = conn.cursor()
        cur.execute("DELETE FROM Rooms WHERE name = %s ;" , (room,) )
        conn.commit()
        cur.close()
        refresh()

def checkin(conn, room, guest, refresh):
    if room == '':
        messagebox.showwarning("Room not selected", "Please select a room to checkin the guest")
    else:
        cur = conn.cursor()
        cur.execute("UPDATE Rooms SET guest = %s, checkin_date = %s WHERE name = %s ;", (guest, date.isoformat(date.today()), room) )
        conn.commit()
        cur.close()
        refresh()

def checkout(conn, room, refresh):
    if room == '' or room == chr(0):
        messagebox.showwarning("Room not selected", "Please select a room to checkout the guest")
    else:
        cur = conn.cursor()
        cur.execute("SELECT checkin_date, price FROM Rooms WHERE name = %s ;", (room,) )
        checkin_date, price = cur.fetchone()
        checkout_date = date.today()
        stay_duration = (checkout_date - checkin_date).days
        if stay_duration == 0:
            stay_duration = 1
        
        cur.execute("UPDATE Rooms SET guest = NULL, checkin_date = NULL WHERE name = %s ;", (room,) )
        conn.commit()
        cur.close()
        
        refresh()
        if stay_duration == 1:
            str_days = " day"
        else:
            str_days = " days"
        messagebox.showinfo("Checkout successfull", "Duration of stay : " + str(stay_duration) + str_days + "\nAmount to be paid : " + str(stay_duration * price) )

def add_tag(conn, tag, refresh):
    tag_list = get_tags(conn)
    if tag == '':
        messagebox.showwarning("Tag name empty", "Please enter a name for the tag")
    elif tag in tag_list:
        messagebox.showwarning("Two tags cannot have the same name", "This tag already exists")
    elif '`' in tag or ';' in tag:
        messagebox.showwarning("Invalid characters in tag name", 'The tag name cannot contain the characters ` or ;')
    else:
        cur = conn.cursor()
        cur.execute('ALTER TABLE Rooms ADD `%s` BOOLEAN DEFAULT FALSE;'%tag, multi = False)
        conn.commit()
        cur.close()
        refresh()

def delete_tag(conn, tag, refresh):
    if tag == '':
        messagebox.showwarning("Tag not selected", "Please select a tag to delete")
    else:
        cur = conn.cursor()
        cur.execute("ALTER TABLE Rooms DROP COLUMN `%s`;"%tag, multi = False)
        conn.commit()
        cur.close()
        refresh()

def assign_tag(conn, room, tag, refresh):
    assigned_tags = get_tags(conn, room)
    
    if room == '':
        messagebox.showwarning("Room not selected", "Please select a room to assign a tag to")
    elif tag == '':
        messagebox.showwarning("Tag not selected", "Please select a tag to assign to the room")
    elif tag in assigned_tags:
        messagebox.showinfo("Tag already assigned", "This room has already been assigned this tag")
    else:
        cur = conn.cursor()
        cur.execute(f"UPDATE Rooms SET `{tag}` = TRUE WHERE name = %s ", (room,), multi = False)
        conn.commit()
        cur.close()
        refresh()

def remove_tag(conn, room, tag, refresh):
    if room == '':
        messagebox.showwarning("Room not selected", "Please select a room to remove a tag from")
    elif tag == '':
        messagebox.showwarning("Tag not selected", "Please select a tag to remove from the room")
    else:
        cur = conn.cursor()
        cur.execute(f"UPDATE Rooms SET `{tag}` = FALSE WHERE name = %s ", (room,), multi = False)
        conn.commit()
        cur.close()
        refresh()

def add_filter(tag, applied_tags, label, optmen_rem_filter, optmen_var):
    if tag in applied_tags:
        messagebox.showinfo("Filter already applied", "This filter has already been applied")
    elif tag == '':
        messagebox.showwarning("Filter not selected", "Please choose a filter to apply")
    else:
        applied_tags.append(tag)
        label.config(text = "Applied Filters : " + ", ".join(applied_tags))
        
        optmen_var.set('')
        optmen_rem_filter['menu'].delete(0, 'end')
        for tag in applied_tags:
            optmen_rem_filter['menu'].add_command(label=tag, command=tk._setit(optmen_var, tag))

def rem_filter(tag, applied_tags, label, optmen_rem_filter, optmen_var):
    if tag == '':
        messagebox.showwarning("Filter not selected", "Please choose a filter to remove")
    else:
        applied_tags.remove(tag)
        label.config(text = "Applied Filters : " + ", ".join(applied_tags))
        
        optmen_var.set('')
        optmen_rem_filter['menu'].delete(0, 'end')
        for tag in applied_tags:
            optmen_rem_filter['menu'].add_command(label=tag, command=tk._setit(optmen_var, tag))

def search(conn, room_name, filters, available, listbox):
    cur = conn.cursor()
    
    statement = "SELECT * FROM Rooms WHERE name LIKE %s"
    for tag in filters:
        statement = statement + f" AND `{tag}` = TRUE"
    if available == 1:
        statement = statement + " AND guest IS NULL"
    statement = statement + ';'
    
    cur.execute(statement, ('%'+room_name+'%', ), multi = False)
    rooms_data = cur.fetchall()
    tag_names = cur.column_names[5:]
    cur.close()
    listbox.delete(0, 'end')

    for room_data in rooms_data:
        list_item = room_data[1] + "     Guest : " + str(room_data[3]) + "     Price : " + str(room_data[2]) + "     Tags :  "
        Flag = False
        for count, tag in enumerate(room_data[5:]):
            if tag:
                list_item = list_item + tag_names[count] + ", "
                Flag = True
        if Flag:
            list_item = list_item[0:-2]

        listbox.insert("end", list_item)

def search_select(conn, room_data, frm_content):
    if room_data == '':
        messagebox.showwarning("Room not selected", "Please select a room")
    else:
        room_name = room_data.split('     ')[0]
        cur = conn.cursor()
        cur.execute("SELECT * FROM Rooms WHERE name = %s", (room_name,))
        room_data = cur.fetchall()[0]
        cur.close()

        display_tab(conn, frm_content, 'specific room', room_data)

def change_name(conn, room_id, old_name, new_name, refresh):
    all_room_names = get_rooms(conn)
    if new_name == '':
        messagebox.showwarning("Room name cannot be empty", "Please enter new name")
    elif new_name == old_name:
        messagebox.showwarning("New name same as old name", "The room's name is already set as the entered name")
    elif new_name in all_room_names:
        messagebox.showwarning("Two rooms cannot have same name", "There is already a room with this name. Please choose another name")
    else:
        cur = conn.cursor()
        cur.execute("UPDATE Rooms SET name = %s WHERE roomid = %s", (new_name, room_id))
        conn.commit()
        cur.close()
        refresh()

def change_price(conn, room_id, new_price, refresh):
    if not new_price.isdigit():
        messagebox.showwarning("Price must be a number", "The price must be a positive whole number")
    else:
        cur = conn.cursor()
        cur.execute("UPDATE Rooms SET price = %s WHERE roomid = %s", (new_price, room_id))
        conn.commit()
        cur.close()
        refresh()
    
if __name__ == "__main__":
    connect()
