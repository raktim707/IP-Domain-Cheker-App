from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SelectFileForm
import ipaddress
import validators

# Create your views here.

def ipaddress_file(request):
    return render(request, 'ipCheck/ipaddress.txt', content_type='text/plain')

def domain_file(request):
    return render(request, 'ipCheck/domains.txt', content_type='text/plain')

def index(request):
    total_domain=None
    total_ip=None
    if request.method == 'GET':
        ip_file = open('ipCheck/templates/ipCheck/ipaddress.txt', 'r')
        file_content = ip_file.read()
        ip_file.close()
        if file_content != '':
            total_ip= len(file_content.split())
        
        domain_file = open('ipCheck/templates/ipCheck/domains.txt', 'r')
        file_content = domain_file.read()
        domain_file.close()
        if file_content != '':
            total_domain = len(file_content.split())
        form = SelectFileForm(request.GET or None)
    elif request.method == 'POST':
        form = SelectFileForm(request.POST)
        ip_list =[]
        public_ips=[]
        duplicates=[]
        domain_list=[]
        rejecteds=[]
        request.session['ip_list'] = 0
        request.session['duplicates'] = 0
        if form.is_valid():
            fileName = form.data['myfile']
            print("File name: ", fileName)
            mytext=form.data['mytext']
            if fileName=='1':
                all_ip_address = mytext.split()
                for i in all_ip_address:
                    try:
                        ip_addr = ipaddress.ip_address(str(i))
                    except:
                        ip_addr=None
                    if ip_addr is not None:
                        if ip_addr.is_private == False:
                            print("Ip address is: ", ip_addr)
                            public_ips.append(str(ip_addr))
                
                public_ips = list(set(public_ips))
                #whitelist ip check
                if len(public_ips) !=0:
                    with open("ipCheck/whitelist.txt", 'r') as file:
                        for addr in file:
                            for ip in public_ips:
                                print("whitelist check: ", ip, addr, (ip ==str(addr).strip()))
                                if ip == str(addr).strip():
                                    print(addr, ip)
                                    rejecteds.append(ip)
                                    break
                
                print("rejecteds: ", rejecteds)               
                if len(rejecteds) !=0:
                    print(rejecteds)
                    ip_list= list(set(public_ips) - set(rejecteds))
                else:
                    ip_list = public_ips
                temp_ip_list=ip_list.copy()
                
                #Duplicate ip check
                if len(ip_list) != 0:
                    with open('ipCheck/templates/ipCheck/ipaddress.txt', 'r') as file:
                        for addr in file:
                            for ip in ip_list:
                                if ip==str(addr).strip():
                                    print("yes, ", ip, str(addr))
                                    ip_list.remove(ip)        
                    duplicates = list(set(temp_ip_list) - set(ip_list)) 
                    print("duplicates are: ", duplicates)
                    request.session['ip_list'] = ip_list  
                    if len(duplicates) != 0:
                        request.session['duplicates'] = duplicates 
                    ip_list = list(set(ip_list))
                    
                    with open('ipCheck/templates/ipCheck/ipaddress.txt', 'a') as file:
                        for ip in ip_list:
                            file.write(str(ip) + "\n")
            
            elif fileName == '2':
                all_domain = mytext.split()
                for item in all_domain:
                    if validators.domain(item):
                        domain_list.append(item)
                
                if len(domain_list) != 0:
                    domain_list = list(set(domain_list))
                
                    with open('ipCheck/whitelist.txt', 'r') as file:
                        for link in file:
                            for domain in domain_list:
                                if str(link).strip() == domain:
                                    domain_list.remove(domain)

                    rejecteds=list(set(all_domain)-set(domain_list))
                    temp_list = domain_list.copy()
                    if len(domain_list) != 0:
                        with open("ipCheck/templates/ipCheck/domains.txt", 'r') as file:
                            for link in file:
                                for domain in domain_list:
                                    if str(link).strip() == domain:
                                        domain_list.remove(domain)
                    
                        duplicates = list(set(temp_list)-set(domain_list))
                    
                        with open("ipCheck/templates/ipCheck/domains.txt", 'a') as file:
                            for domain in domain_list:
                                file.write(domain + "\n")
                          
        context={
            'filename': fileName,
            'duplicates':duplicates,
            'ip_list': ip_list,
            'rejecteds': rejecteds,
            'domain_list': domain_list
        }
        return render(request, "ipCheck/result.html", context=context) 
                    
    return render(request, "ipCheck/index.html", {'form':form, 'total_ip':total_ip, 'total_domain':total_domain})
    