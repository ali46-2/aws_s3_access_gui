from tkinter import *
from tkinter import filedialog, font, messagebox
import boto3
import botocore
import os


def upload_file(bucket_name, access_key, secret_access_key):
    if bucket_name == "" or access_key == "" or secret_access_key == "":
        messagebox.showinfo("Info", "Please fill in all details!")
        return

    window = filedialog.askopenfilename()
    if window:
        file_path = open(window, "r").name
        file_name = os.path.basename(file_path)
        client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_access_key
        )
        try:
            client.upload_file(file_path, bucket_name, file_name)
        except boto3.exceptions.S3UploadFailedError as error:
            messagebox.showinfo("Error", str(error).split(":")[-1])


def save_file(bucket_name, access_key, secret_access_key, file_name):
    path = filedialog.askdirectory()
    if path:
        client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_access_key
        )
        client.download_file(bucket_name, file_name, os.path.join(path, file_name))


def delete_file(bucket_name, access_key, secret_access_key, listbox):
    client = boto3.client(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_access_key
    )
    client.delete_object(Bucket=bucket_name, Key=listbox.get(ANCHOR))
    listbox.delete(ANCHOR)


def new_window(bucket_name, access_key, secret_access_key):
    if bucket_name == "" or access_key == "" or secret_access_key == "":
        messagebox.showinfo("Info", "Please fill in all details!")
        return

    client = boto3.client(
        "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_access_key
    )
    try:
        all_objects = client.list_objects(Bucket=bucket_name)
    except botocore.exceptions.ClientError as error:
        messagebox.showinfo("Error", error.response["Error"]["Message"])
        print(error.response["Error"]["Message"])
        return

    if "Contents" not in all_objects:
        messagebox.showinfo("Info", "Bucket is empty!")
        return

    top = Toplevel()
    top.grab_set()
    top.configure(background="#471344")
    top.minsize(400, 500)
    top.title("Download/Delete")

    list_frame = Frame(top, bg="#471344")
    list_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    listbox = Listbox(list_frame, bg="white", fg="black")

    for i in all_objects["Contents"]:
        listbox.insert(END, i["Key"])

    listbox.pack(pady=10)

    download = Button(
        list_frame,
        text="Download",
        width=10,
        bg="#6e2369",
        fg="white",
        activebackground="#6e2369",
        activeforeground="white",
        command=lambda: save_file(
            bucket_name, access_key, secret_access_key, listbox.get(ANCHOR)
        ),
    )
    delete = Button(
        list_frame,
        text="Delete",
        width=10,
        bg="#6e2369",
        fg="white",
        activebackground="#6e2369",
        activeforeground="white",
        command=lambda: delete_file(
            bucket_name, access_key, secret_access_key, listbox
        ),
    )

    download.pack(pady=10)
    delete.pack(pady=10)


# Root
root = Tk()
root.configure(background="#471344")
root.title("AWS S3 Access")
root.minsize(700, 400)

default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Monoton", size=14, weight=font.BOLD)

# Main frame
main_frame = Frame(root)
main_frame.configure(background="#471344")
main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# First frame
first_frame = Frame(main_frame, padx=20, pady=20)
first_frame.configure(background="#471344")

access_key_label = Label(first_frame, text="Access Key ID:", bg="#471344", fg="white")
access_key_entry = Entry(first_frame, width=30, font=("Monoton", 14))

secret_access_key_label = Label(
    first_frame, text="Secret Access Key:", bg="#471344", fg="white"
)
secret_access_key_entry = Entry(first_frame, show="*", width=30, font=("Monoton", 14))

bucket_name_label = Label(first_frame, text="Bucket Name:", bg="#471344", fg="white")
bucket_name_entry = Entry(first_frame, width=30, font=("Monoton", 14))

access_key_label.grid(row=0, column=0)
access_key_entry.grid(row=0, column=1)

secret_access_key_label.grid(row=1, column=0, pady=(15, 15))
secret_access_key_entry.grid(row=1, column=1, pady=(15, 15))

bucket_name_label.grid(row=2, column=0)
bucket_name_entry.grid(row=2, column=1)

first_frame.grid(row=0, column=0)

# Second frame
second_frame = Frame(main_frame, padx=20, pady=20)
second_frame.configure(background="#471344")

upload = Button(
    second_frame,
    text="Upload",
    width=15,
    height=2,
    bg="#6e2369",
    fg="white",
    activebackground="#6e2369",
    activeforeground="white",
    command=lambda: upload_file(
        bucket_name_entry.get(), access_key_entry.get(), secret_access_key_entry.get()
    ),
)
access = Button(
    second_frame,
    text="Download/Delete",
    width=15,
    bg="#6e2369",
    fg="white",
    activebackground="#6e2369",
    activeforeground="white",
    height=2,
    command=lambda: new_window(
        bucket_name_entry.get(), access_key_entry.get(), secret_access_key_entry.get()
    ),
)

upload.grid(row=0, column=0, padx=(0, 30))
access.grid(row=0, column=1, padx=(30, 0))

second_frame.grid(row=1, column=0, pady=(50, 0))

root.mainloop()
