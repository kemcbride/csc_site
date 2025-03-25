# my csc website

hi!

this is just where i can keep track of changes that I make. mostly there is no plan.
except for that there is somewhat of a plan.

### plan part 1:

all the stuff i wrote on the index page, about putting neopets stuff there.
i think it'd still be very nice for me to do that.

### plan part 2:

the in the groove stuff! all the stuff in and around itg2/

this stuff is all mostly just a me-pretending-to-do-my-own groovestats.com.
so all the scores there are mine, or from my usb sticks. wah wah wah.

there are a couple of branches for that.

#### database stuff

wouldn't that be cool? to make it be a real really real database?

#### javascript/frontendy stuff

wouldn't THAT be cool? an actually cool visualization stuff?
and also can work with the database maybe even??? who knows.

#### caching or something

wouldn't THAAT be cool? yeah. maybe.
idk. we'll see.


### Useful commands

`time sudo docker build -t csc_site_image . --platform linux/x86_64`
- Most of the builds I was trying (to use arm64) were failing with vague errors (no logs, pip install -r requirements.txt failed with error code 159), but this one is finally working.
- Yes, I'm basing it crurently on jupyter/minimal-notebook, so i am getting extra jupyter packages, but at least pandas & numpy are there and it's working.
- I might try on a slimmer build some time soon now that i feel better about using other arches.

- Run via docker:
`sudo docker run -p "25777:25777" --name csc_site -d csc_site_image`
- Note: the name of the image MUST go at the end!

- Add group cpu/memory limits to the pi? https://dalwar23.com/how-to-fix-no-memory-limit-support-for-docker-in-raspberry-pi/
```
  nano /boot/firmware/cmdline.txt
cgroup_enable=memory swapaccount=1 cgroup_memory=1 cgroup_enable=cpuset
```
