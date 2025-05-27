function hover(){
    const hoverDivs = document.querySelectorAll('.hover-effect');
    let comment = document.querySelector('#commentaire');
    hoverDivs.forEach(div => {
        div.addEventListener('mouseover', () => {
            if(div.id === "passiveRecon")
            {   
                console.log("Mouse over passive reconnaissance");
                comment.innerHTML = "Passive reconnaissance is the process of gathering information about a target without direct interaction, often using publicly available data.";
            }
            else if(div.id === "nmapResult")
            {
                console.log("Mouse over Nmap results");
                comment.innerHTML = "Nmap results provide detailed information about the network, including open ports, services running, and potential vulnerabilities.";
            }
            else if( div.id === "exploitResult")
            {
                console.log("Mouse over exploit results");
                comment.innerHTML = "Exploit results show the outcome of attempts to exploit vulnerabilities in the target system, indicating success or failure.";
            }
            else if(div.id === "zapResult")
            {
                console.log("Mouse over ZAP results");
                comment.innerHTML = "ZAP results provide insights into security vulnerabilities found in web applications, including potential risks and recommended actions.";
            }

        });
        div.addEventListener('mouseout', () => {
            comment.innerHTML = '';
            
            console.log("Mouse out of " + div.id);
        });
    });
}

function main(){
    hover();
}

main();