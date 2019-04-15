import lirc

sockid = lirc.init("dashboard")
print(lirc.nextcode())
lirc.deinit()