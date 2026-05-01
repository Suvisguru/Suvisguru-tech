# Lesson 04 — A short history of virtualization

*Course: vSphere Fundamentals · Domain: VMware · Position: 04*

---

## 1. Concept explanation

Virtualization isn't new. It's older than personal computers. The technology you use today — vSphere, AWS EC2, Azure VMs — descends from work IBM did on mainframes in the 1960s.

The story has eight beats.

**1960s.** IBM builds CP/CMS, the first hypervisor, on its System/360 mainframes. The goal: let one $20-million machine support many users running independently. The hypervisor on a mainframe is called a *virtual machine monitor*; the term "virtual machine" is born here.

**1970s-80s.** Virtualization stays mainframe-only. PCs and servers run one OS at a time. The idea is dormant outside big-iron datacenters.

**1998.** Five Stanford researchers (Diane Greene, Mendel Rosenblum, Edouard Bugnion, Scott Devine, Edward Wang) found VMware. Their insight: the techniques that worked on mainframes can work on commodity x86 hardware too. This was not obvious at the time.

**1999.** VMware Workstation ships — a Type-2 hypervisor for desktop x86. Developers can run multiple OSes on a single PC.

**2001.** VMware ESX Server ships — the first Type-1 hypervisor for x86 servers. This is the moment virtualization moves from a curiosity to enterprise infrastructure.

**2003.** vMotion ships. VMs can move between hosts while running. The "magical" capability becomes real.

**2006.** AWS launches EC2. Public cloud is built on virtualization.

**2013.** Docker popularizes containers — a different abstraction that runs alongside virtualization, not as a replacement. Most production container workloads run on top of VMs to this day.

The throughline: each era took an idea that worked at one scale and made it work at the next scale up.

---

## 2. Before / after

**Before VMware (pre-1998 on x86).** A mid-sized company runs Windows NT, Linux, NetWare on dedicated physical servers. Buying a server is a capital purchase. Refresh cycles are three years. Disaster recovery means warm-spare hardware sitting in another room. The only people getting "many OSes on one box" are the ones running mainframes — and those cost millions.

**After VMware (post-2001).** The same company runs the same workloads as VMs on a fraction of the hardware. New workloads come up in minutes. Disaster recovery is replicating VM files. The mainframe-class capability is now available on commodity x86 servers that cost a tenth of what mainframes did. Twenty years later, public cloud takes the same model and rents it by the second.

---

## 3. Analogy — the city, over time

The apartment-building analogy from Lesson 1 is itself a piece of history.

In the 1960s, only a few cities had skyscrapers — and they were the financial capitals. Mainframes were the same: a few institutions had them, and only big ones could afford the elevators, the structural engineering, the maintenance.

In 1998 VMware figured out how to build a small apartment building on a regular street, using ordinary materials. Suddenly any city could have one. By 2005, apartment buildings were the default for new construction. By 2010, the cloud era was every-skyscraper-everywhere.

What we today call "the cloud" is just a city of skyscrapers, where anyone can rent an apartment by the day. The bones of every skyscraper are still virtualization.

---

## 4. ELI5 and ELI10

### ELI5

Long ago, only really big computers (mainframes) could pretend to be lots of computers. Then in 1998, a company called VMware figured out how to make small computers do the same trick. Soon every company was using it. Now the cloud — Amazon, Google, Microsoft — runs the same trick at a giant scale. So the cloud is built on virtualization that is built on a 60-year-old idea.

### ELI10

Virtualization originated on IBM mainframes in the 1960s, where a hypervisor called CP/CMS let one expensive mainframe support many independent users running their own operating systems. The technology stayed mainframe-only for thirty years because nobody knew how to apply it to commodity x86 hardware — which has architectural quirks (privileged instruction handling, memory management) that mainframes don't.

In 1998 VMware solved the x86 problem. VMware Workstation (1999) brought hypervisors to desktops; ESX Server (2001) brought them to commodity datacenter servers. Live migration (vMotion, 2003) made workloads movable while running. By the late 2000s most enterprises were virtualized. AWS (2006), Azure (2010), and GCP (2008) all built their compute services on virtualization at hyperscale. Containers (Docker, 2013) added a lighter-weight abstraction that mostly runs <em>on top of</em> VMs, not instead of them. Today virtualization is invisible infrastructure under nearly every internet-facing service.

---

## 5. Real-world scenarios

### A 1972 bank — virtualization, the original use case

Chase Manhattan Bank in 1972 runs an IBM 370 mainframe with CP/CMS. Eighty programmers each get their own *virtual* mainframe through CP/CMS. Each programmer's CMS session sees its own RAM, disks, and devices. The hypervisor schedules them all on the one physical machine. It works. Mainframes will be the only place this works for the next 25 years.

### A 2001 startup — early-adopter VMware

A small ISP in 2001 buys two ESX Server licenses and consolidates 14 dedicated Linux boxes onto two beefier hosts. Operations cost drops by 60%. The ISP has no idea they're using technology that won't be standard for another five years.

### A 2006 enterprise — pre-cloud peak VMware

A 5,000-employee insurance company in 2006 has standardized on VMware vSphere. Their datacenter is 80% virtual, 20% legacy physical. They start migrating disaster recovery to a second site using VM replication — a workflow that was impossible without virtualization. Two months later, AWS launches EC2 publicly. The insurance company doesn't notice yet.

### A 2024 SaaS — virtualization invisible underneath

A 100-person SaaS in 2024 deploys an application to AWS Fargate, with managed databases on RDS and caching on ElastiCache. The CTO has never logged into a hypervisor. They don't need to know virtualization exists. But every container they run, every database they create, every cache node — sits inside a VM running on a hypervisor that AWS operates. Virtualization made the whole experience possible; it's just invisible.

---

## 6. Animated illustration

Open `animation.html` for the interactive timeline. Drag through the years to see what was happening at each milestone, or step from era to era. The static `diagram.svg` shows the same timeline as a single composition.

---

## 7. Flashcards and quiz

Ten flashcards in `flashcards.yaml` cover key milestones, founders, and the relationship between virtualization, mainframes, and cloud. Three quiz questions in `quiz.yaml` test prediction across eras.
