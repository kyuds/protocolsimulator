# protocol simulator

### Getting Started
```
git clone git@github.com:kyuds/protocolsimulator.git
conda create --name protocol --file requirements.txt
```

### Protocols
There are two protocols for determining locations to perform remote spill. One, we can use the common technique, Power of Two Choices, and second, we can use the Chord network load balancer. Since Power of Two Choices relies on random chance to perform properly, we wanted to see if using Chord to find remote spill locations would incur performance benefits.
