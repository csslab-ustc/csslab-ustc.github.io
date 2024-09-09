
#include<stdio.h>
#include<string.h>
#include<malloc.h>
#include<errno.h>

#include<sys/socket.h>
#include<sys/types.h>
#include<sys/ioctl.h>

#include<net/if.h>
#include<netinet/in.h>
#include<netinet/ip.h>
#include<netinet/if_ether.h>
#include<netinet/udp.h>
#include<netinet/tcp.h>
#include<linux/if_packet.h>

#include<arpa/inet.h>
struct ifreq ifreq_c,ifreq_i,ifreq_ip; /// for each ioctl keep diffrent ifreq structure otherwise error may come in sending(sendto )
int sock_raw;
unsigned char *sendbuff;
 
 #define DESTMAC0	0x00
 #define DESTMAC1	0x0c
 #define DESTMAC2	0x29
 #define DESTMAC3	0xe1
 #define DESTMAC4	0x8c
 #define DESTMAC5	0xaa
 
 #define destination_ip 192.168.117.138

int total_len=0,send_len;


struct pseudo_tcp{
        unsigned int saddr, daddr;
	unsigned char mbz;
	unsigned char ptcl;
	unsigned short tcpl;
	struct tcphdr tcp;
	//char payload[5];   // increase in case of large data.Here data is --> AA  BB  CC  DD  EE
};


struct pseudo_tcp p_tcp;




unsigned short checksum(unsigned char* buf, int size) {
	unsigned int checkSum = 0;
	for (int i = 0; i < size; i += 2) {
		unsigned short first = (unsigned short)buf[i] << 8;
		unsigned short second = (unsigned short)buf[i+1] & 0x00ff;
		checkSum += first + second;
	}
	while (1) {
		unsigned short c = (checkSum >> 16);
		if (c > 0) {
			checkSum = (checkSum << 16) >> 16;
			checkSum += c;
		} else {
			break;
		}
	}
	return ~checkSum;
}




unsigned short tcp_checksum(struct tcphdr *tcp){
	int tcp_len = sizeof(struct tcphdr);
	p_tcp.mbz = 0;
	p_tcp.ptcl = IPPROTO_TCP;
	p_tcp.tcpl = htons(tcp_len);
	memcpy(&p_tcp.tcp, tcp, tcp_len);
	return (unsigned short) checksum((unsigned char *)&p_tcp, sizeof(struct pseudo_tcp));
}


void get_eth_index()
{
	memset(&ifreq_i,0,sizeof(ifreq_i));
	strncpy(ifreq_i.ifr_name,"ens33",IFNAMSIZ-1);

	if((ioctl(sock_raw,SIOCGIFINDEX,&ifreq_i))<0)
		printf("error in index ioctl reading");

	printf("index=%d\n",ifreq_i.ifr_ifindex);

}

void get_mac()
{
	memset(&ifreq_c,0,sizeof(ifreq_c));
	strncpy(ifreq_c.ifr_name,"ens33",IFNAMSIZ-1);

	if((ioctl(sock_raw,SIOCGIFHWADDR,&ifreq_c))<0)
		printf("error in SIOCGIFHWADDR ioctl reading");

	printf("Mac= %.2X-%.2X-%.2X-%.2X-%.2X-%.2X\n",(unsigned char)(ifreq_c.ifr_hwaddr.sa_data[0]),(unsigned char)(ifreq_c.ifr_hwaddr.sa_data[1]),(unsigned char)(ifreq_c.ifr_hwaddr.sa_data[2]),(unsigned char)(ifreq_c.ifr_hwaddr.sa_data[3]),(unsigned char)(ifreq_c.ifr_hwaddr.sa_data[4]),(unsigned char)(ifreq_c.ifr_hwaddr.sa_data[5]));

	
	printf("ethernet packaging start ... \n");
	
	struct ethhdr *eth = (struct ethhdr *)(sendbuff);
  	eth->h_source[0] = (unsigned char)(ifreq_c.ifr_hwaddr.sa_data[0]);
  	eth->h_source[1] = (unsigned char)(ifreq_c.ifr_hwaddr.sa_data[1]);
   	eth->h_source[2] = (unsigned char)(ifreq_c.ifr_hwaddr.sa_data[2]);
   	eth->h_source[3] = (unsigned char)(ifreq_c.ifr_hwaddr.sa_data[3]);
   	eth->h_source[4] = (unsigned char)(ifreq_c.ifr_hwaddr.sa_data[4]);
   	eth->h_source[5] = (unsigned char)(ifreq_c.ifr_hwaddr.sa_data[5]);

   	eth->h_dest[0]    =  DESTMAC0;
   	eth->h_dest[1]    =  DESTMAC1;
   	eth->h_dest[2]    =  DESTMAC2;
  	eth->h_dest[3]    =  DESTMAC3;
   	eth->h_dest[4]    =  DESTMAC4;
   	eth->h_dest[5]    =  DESTMAC5;

   	eth->h_proto = htons(ETH_P_IP);   //0x0800

   	printf("ethernet packaging done.\n");

	total_len+=sizeof(struct ethhdr);


}

void get_data()
{
	sendbuff[total_len++]	=	0xAA;
	sendbuff[total_len++]	=	0xBB;
	sendbuff[total_len++]	=	0xCC;
	sendbuff[total_len++]	=	0xDD;
	sendbuff[total_len++]	=	0xEE;

}


void get_udp()
{
	struct udphdr *uh = (struct udphdr *)(sendbuff + sizeof(struct iphdr) + sizeof(struct ethhdr));

	uh->source	= htons(23451);
	uh->dest	= htons(23452);
	uh->check	= 0;

	total_len+= sizeof(struct udphdr);
	get_data();
	uh->len		= htons((total_len - sizeof(struct iphdr) - sizeof(struct ethhdr)));

}


void get_tcp()
{
	struct tcphdr *th = (struct tcphdr *)(sendbuff + sizeof(struct iphdr) + sizeof(struct ethhdr));

	th->source	= htons(23451);
	th->dest	= htons(23452);
	th->seq	        = htonl(1111);
	th->ack_seq	= htonl(0);
	th->urg         = 0;
	th->ack         = 0;
	th->psh         = 0;
	th->rst         = 0;
	th->syn         = 1;
	th->fin         = 0;
	th->window      = htons(14600);
	th->check       = 0;
	th->urg_ptr     = htons(0);
	th->doff        = 5;
	total_len += sizeof(struct tcphdr);
	//get_data();
	th->check       = htons(tcp_checksum(th));
	printf("check:%.2X\n",th->check);
}

 
void get_ip()
{
	memset(&ifreq_ip,0,sizeof(ifreq_ip));
	strncpy(ifreq_ip.ifr_name,"ens33",IFNAMSIZ-1);
  	 if(ioctl(sock_raw,SIOCGIFADDR,&ifreq_ip)<0)
 	 {
		printf("error in SIOCGIFADDR \n");
	 }
	
	printf("%s\n",inet_ntoa((((struct sockaddr_in*)&(ifreq_ip.ifr_addr))->sin_addr)));

	memset(&p_tcp, 0x0, sizeof(struct pseudo_tcp));
	struct iphdr *iph = (struct iphdr*)(sendbuff + sizeof(struct ethhdr));
	iph->ihl	= 5;
	iph->version	= 4;
	iph->tos	= 16;
	iph->id		= htons(10201);
	iph->ttl	= 64;
	iph->protocol	= IPPROTO_TCP;
	iph->saddr	= inet_addr(inet_ntoa((((struct sockaddr_in *)&(ifreq_ip.ifr_addr))->sin_addr)));
	p_tcp.saddr	= inet_addr(inet_ntoa((((struct sockaddr_in *)&(ifreq_ip.ifr_addr))->sin_addr)));	
	iph->daddr	= inet_addr("192.168.117.138"); // put destination IP address
	p_tcp.daddr	= inet_addr("192.168.117.138");
	total_len += sizeof(struct iphdr); 
	get_tcp();

	iph->tot_len	= htons(total_len - sizeof(struct ethhdr));
	iph->check	= htons(checksum((unsigned char*)(sendbuff + sizeof(struct ethhdr)), sizeof(struct iphdr)));
}




int main()
{
	sock_raw=socket(AF_PACKET,SOCK_RAW,ETH_P_IP);
	if(sock_raw == -1)
		printf("error in socket");

	sendbuff=(unsigned char*)malloc(64); // increase in case of large data.Here data is --> AA  BB  CC  DD  EE
	memset(sendbuff,0,64);


	get_eth_index();  // interface number
	get_mac();
	get_ip();

	struct sockaddr_ll sadr_ll;

	sadr_ll.sll_ifindex = ifreq_i.ifr_ifindex;
	sadr_ll.sll_halen   = ETH_ALEN;
	sadr_ll.sll_addr[0]  = DESTMAC0;
	sadr_ll.sll_addr[1]  = DESTMAC1;
	sadr_ll.sll_addr[2]  = DESTMAC2;
	sadr_ll.sll_addr[3]  = DESTMAC3;
	sadr_ll.sll_addr[4]  = DESTMAC4;
	sadr_ll.sll_addr[5]  = DESTMAC5;
	int count = 0;
	printf("sending...\n");
	while(1)
	{
		//count++;
		if (count > 100){
			return 0;	
		}
		send_len = sendto(sock_raw,sendbuff,64,0,(const struct sockaddr*)&sadr_ll,sizeof(struct sockaddr_ll));
		if(send_len<0)
		{
			printf("error in sending....sendlen=%d....errno=%d\n",send_len,errno);
			return -1;

		}

	}



}
