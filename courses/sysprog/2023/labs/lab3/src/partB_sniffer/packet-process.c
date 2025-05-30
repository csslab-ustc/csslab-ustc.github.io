#include <stdio.h>
#include <string.h>
#include <net/ethernet.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <netinet/ip_icmp.h>
#include <netinet/if_ether.h>
#include "packet-process.h"

struct sockaddr_in source, dest;
int total = 0, tcp = 0, udp = 0, icmp = 0, igmp = 0, other = 0, arp_packet = 0;
int ipheader_len;

// packet print
void packet_print(unsigned char* buffer,int buffer_len){
    printf("\n---------------------------- Packet ----------------------------\n");
    for(int i=0; i<buffer_len; i++){
        if(i!=0 && i%16==0)
            printf("\n");
        printf(" %.2X ",buffer[i]);
    }

    printf("\n----------------------- Packet finished ------------------------");
}

// print format of etherNet-header
void mac_header(unsigned char *buffer, int buffer_len){
    struct ethhdr *eth = (struct ethhdr*)(buffer);
    printf("\nEthernet Header\n");
    printf("\t|-Source Address      : %.2x-%.2x-%.2x-%.2x-%.2x-%.2x\n",
           eth->h_source[0], eth->h_source[1], eth->h_source[2],
           eth->h_source[3], eth->h_source[4], eth->h_source[5]);
    printf("\t|-Destination Address : %.2x-%.2x-%.2x-%.2x-%.2x-%.2x\n",
           eth->h_dest[0], eth->h_dest[1], eth->h_dest[2],
           eth->h_dest[3], eth->h_dest[4], eth->h_dest[5]);
    printf("\t|-Protocol            : %d\n", eth->h_proto);
}

// print format of arp-header
void arp_header(unsigned char *buffer, int buffer_len){
    struct arphdr *arp = (struct arphdr*)(buffer +sizeof(struct ethhdr));
    printf("\nARP Header\n");
    printf("\t|-Format of Hardware Address      : %d\n", (unsigned int)arp->ar_hrd);
    printf("\t|-Format of Protocol Address      : %.4x\n", (unsigned int)arp->ar_pro);
    printf("\t|-Length of Hardware Address      : %c\n", arp->ar_hln);
    printf("\t|-Length of Protocol Address      : %c\n", arp->ar_pln);
    printf("\t|-ARP opcode:                     : %d\n", (unsigned int)arp->ar_op);
}

// print format of ip-header
void ip_header(unsigned char *buffer, int buffer_len){
    struct iphdr *ip = (struct iphdr*)(buffer +sizeof(struct ethhdr));
    ipheader_len = ip->ihl*4;

    memset(&source, 0, sizeof(source));
    source.sin_addr.s_addr = ip->saddr;
    memset(&dest, 0, sizeof(dest));
    dest.sin_addr.s_addr = ip->daddr;

    printf("\nIP Header\n");
    printf("\t|-Version                 : %d\n", (unsigned int)ip->version);
    printf("\t|-Internet Header Length  : %d DWORDS or %d Bytes\n",
           (unsigned int)ip->ihl, ((unsigned int)(ip->ihl))*4);
    printf("\t|-Type of Service         : %d\n", (unsigned int)ip->tos);
    printf("\t|-Total length            : %d Bytes\n", ntohs(ip->tot_len));
    printf("\t|-Identification          : %d\n", ntohs(ip->id));
    printf("\t|-TTL                     : %d\n", (unsigned int)ip->ttl);
    printf("\t|-Protocol                : %d\n", (unsigned int)ip->protocol);
    printf("\t|-Header Checksum         : %d\n", ntohs(ip->check));
    printf("\t|-Source IP               : %s\n", inet_ntoa(source.sin_addr));
    printf("\t|-Destination IP          : %s\n", inet_ntoa(dest.sin_addr));
}

// print format of tcp-header
void tcp_header(unsigned char* buffer, int buffer_len){
    struct tcphdr *tcp = (struct tcphdr*)(buffer + ipheader_len + sizeof(struct ethhdr));
    printf("\nTCP Header\n");
    printf("\t|-Source Port             : %u\n",ntohs(tcp->source));
    printf("\t|-Destination Port        : %u\n",ntohs(tcp->dest));
    printf("\t|-Sequence Number         : %u\n",ntohl(tcp->seq));
    printf("\t|-Acknowledge Number      : %u\n",ntohl(tcp->ack_seq));
    printf("\t|-Header Length           : %d DWORDS or %d BYTES\n" ,
           (unsigned int)tcp->doff,(unsigned int)tcp->doff*4);
    printf("\t|----------Flags-----------\n");
    printf("\t\t|-Urgent Flag          : %d\n",(unsigned int)tcp->urg);
    printf("\t\t|-Acknowledgement Flag : %d\n",(unsigned int)tcp->ack);
    printf("\t\t|-Push Flag            : %d\n",(unsigned int)tcp->psh);
    printf("\t\t|-Reset Flag           : %d\n",(unsigned int)tcp->rst);
    printf("\t\t|-Synchronise Flag     : %d\n",(unsigned int)tcp->syn);
    printf("\t\t|-Finish Flag          : %d\n",(unsigned int)tcp->fin);
    printf("\t|-Window size             : %d\n",ntohs(tcp->window));
    printf("\t|-Checksum                : %d\n",ntohs(tcp->check));
    printf("\t|-Urgent Pointer          : %d\n",tcp->urg_ptr);
}

// print format of udp-header
void udp_header(unsigned char* buffer, int buffer_len){
    struct udphdr *udp = (struct udphdr*)(buffer + ipheader_len + sizeof(struct ethhdr));
    printf("\nUDP Header\n");
    printf("\t|-Source Port    	      : %d\n" , ntohs(udp->source));
    printf("\t|-Destination Port	      : %d\n" , ntohs(udp->dest));
    printf("\t|-UDP Length      	      : %d\n" , ntohs(udp->len));
    printf("\t|-UDP Checksum   	      : %d\n" , ntohs(udp->check));
}

// print format of icmp-header
void icmp_header(unsigned char *buffer, int buffer_len){
    struct icmp *icmp_packet = (struct icmp*)(buffer + ipheader_len + sizeof(struct ethhdr));
    printf("\nICMP Header\n");
    printf("\t|-TYPE                    : %d\n",icmp_packet->icmp_type);
    printf("\t|-CODE                    : %d\n",icmp_packet->icmp_code);
    printf("\t|-CHECKSUM                : %d\n",ntohs(icmp_packet->icmp_cksum));
}

// print format of payload
void payload(unsigned char* buffer,int buffer_len){
    unsigned char *data = (buffer + ipheader_len  + sizeof(struct ethhdr) + sizeof(struct udphdr));

    printf("\nData\n");
    int data_len = buffer_len - (ipheader_len  + sizeof(struct ethhdr) + sizeof(struct udphdr));
    for(int i=0; i<data_len; i++){
        if(i!=0 && i%16==0)
            printf("\n");
        printf(" %.2X ",data[i]);
    }

    printf("\n");
}

// print ICMP packet
void ICMP_printer(unsigned char *buffer, int buffer_len){
    printf("\n---------------------------ICMP Packet---------------------------");
    // print header
    mac_header(buffer,buffer_len);
    ip_header(buffer,buffer_len);
    icmp_header(buffer, buffer_len);
    // print packet payload
    payload(buffer, buffer_len);
    printf("--------------------------------------------------------------\n\n\n");
}

// print ARP packet
void ARP_printer(unsigned char *buffer, int buffer_len){
    printf("\n---------------------------ARP Packet---------------------------");
    // print header
    mac_header(buffer, buffer_len);
    arp_header(buffer, buffer_len);
    // print payload
    struct ether_arp *arp = (struct ether_arp*)(buffer +sizeof(struct ethhdr));
    printf("\t|-Sender Hardware Address      : %.2x-%.2x-%.2x-%.2x-%.2x-%.2x\n",
           arp->arp_sha[0], arp->arp_sha[1], arp->arp_sha[2],
           arp->arp_sha[3], arp->arp_sha[4], arp->arp_sha[5]);
    printf("\t|-Sender Protocol Address      : %d.%d.%d.%d\n",
           arp->arp_sha[0],arp->arp_sha[1],arp->arp_sha[2],arp->arp_sha[3]);
    printf("\t|-Target Hardware Address      : %.2x-%.2x-%.2x-%.2x-%.2x-%.2x\n",
           arp->arp_tha[0], arp->arp_tha[1], arp->arp_tha[2],
           arp->arp_tha[3], arp->arp_tha[4], arp->arp_tha[5]);
    printf("\t|-Target Protocol Address      : %d.%d.%d.%d\n",
           arp->arp_tpa[0],arp->arp_tpa[1],arp->arp_tpa[2],arp->arp_tpa[3]);
}

// print TCP packet
void TCP_printer(unsigned char *buffer, int buffer_len){
    printf("\n---------------------------TCP Packet---------------------------");
    // print header
    mac_header(buffer, buffer_len);
    ip_header(buffer, buffer_len);
    tcp_header(buffer, buffer_len);
    // print packet payload
    payload(buffer,buffer_len);


    printf("--------------------------------------------------------------\n\n\n");
}

// print UDP packet
void UDP_printer(unsigned char* buffer, int buffer_len){
    printf("\n---------------------------UDP Packet---------------------------");
    // print header
    mac_header(buffer,buffer_len);
    ip_header(buffer,buffer_len);
    udp_header(buffer, buffer_len);
    // print packet payload
    payload(buffer,buffer_len);

    printf("--------------------------------------------------------------\n\n\n");
}

// packet process func
void packet_process(unsigned char* buffer, int buffer_len){
    ++total;
    struct ethhdr *eth = (struct ethhdr*)(buffer);
    struct iphdr *ip = (struct iphdr*)(buffer + sizeof(struct ethhdr));
    switch((int) ntohs(eth->h_proto)){
        case 0x0800:  // 0800 -> ip
            switch(ip->protocol){
                case 1:                                     // ICMP packet
                    ++icmp;
                    ICMP_printer(buffer, buffer_len);
                    break;

                case 2:
                    ++igmp;
                    break;

                case 6:                                     // TCP packet
                    ++tcp;
                    TCP_printer(buffer, buffer_len);         // print packet info
                    break;

                case 17:                                    // UDP packet
                    ++udp;
                    UDP_printer(buffer,buffer_len);          // print packet info
                    break;

                default:
                    ++other;
            }
            break;

        case 0x0806:  // 0806 -> arp
            ++arp_packet;
            ARP_printer(buffer, buffer_len);            // print ARP packet info
            break;

        default:
            ++other;
    }

    printf("Result: [TCP : %d], [UDP : %d], [ARP : %d], [ICMP : %d], [IGMP : %d], [OTHER : %d], [TOTAL : %d]\n",
           tcp, udp, arp_packet, icmp, igmp, other, total);
}