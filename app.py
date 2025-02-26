import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.set_page_config(
        page_title="Virtual Machines and Memory Virtualization",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1E3A8A;
                margin-bottom: 1.5rem;
                text-align: center;
            }
            .section-header {
                font-size: 1.8rem;
                font-weight: bold;
                color: #2563EB;
                margin-top: 2rem;
                margin-bottom: 1rem;
                border-bottom: 2px solid #BFDBFE;
                padding-bottom: 0.5rem;
            }
            .subsection-header {
                font-size: 1.4rem;
                font-weight: bold;
                color: #3B82F6;
                margin-top: 1.5rem;
                margin-bottom: 0.8rem;
            }
            .text-content {
                font-size: 1.1rem;
                line-height: 1.6;
                text-align: justify;
                margin-bottom: 1.2rem;
            }
            .highlight-term {
                font-weight: bold;
                color: #1D4ED8;
                background-color: #EFF6FF;
                padding: 0 0.3rem;
                border-radius: 0.2rem;
            }
            .sidebar-content {
                padding: 1rem;
                background-color: #F3F4F6;
                border-radius: 0.5rem;
            }
            .definition-box {
                background-color: #DBEAFE;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 4px solid #2563EB;
                margin-top: 0.5rem;
            }
            .references {
                font-size: 0.9rem;
                line-height: 1.4;
            }
        </style>
    """, unsafe_allow_html=True)

    # Terminology database
    terminology = {
        "Cache Coherence": "Ensures all CPU caches maintain a consistent view of memory.",
        "Full Virtualization": "A method where the VMM completely emulates hardware so that an unmodified guest OS can run.",
        "Hardware-Assisted Virtualization": "CPU features that provide direct support for virtualization, reducing the need for software-based emulation (e.g., Intel VT-x, AMD-V).",
        "Host OS vs. Guest OS": "The host OS is the primary operating system running on the physical machine, while the guest OS runs within a virtual machine.",
        "Live Migration": "The process of moving a running VM from one physical host to another without downtime.",
        "Memory Management Unit (MMU)": "A hardware component that translates virtual addresses into physical addresses.",
        "Page Fault": "Occurs when a requested page is not in physical memory, requiring the OS to fetch it from disk.",
        "Page Table": "A data structure used by the OS to map virtual addresses to physical addresses.",
        "Paging": "A memory management scheme that divides virtual memory into fixed-size units called pages.",
        "Paravirtualization": "A virtualization method where the guest OS is modified to work efficiently with the hypervisor.",
        "Resource Sharing": "Multiple VMs share hardware resources such as CPU, memory, and storage, improving utilization.",
        "Snooping Protocol": "A cache coherence mechanism where caches monitor the bus for changes.",
        "Trap-and-Emulate": "A method where the VMM intercepts privileged instructions executed by the guest OS and safely emulates them.",
        "Translation Lookaside Buffer (TLB)": "A cache that stores recent virtual-to-physical address mappings to speed up address translation.",
        "Type 1 Hypervisor (Bare Metal)": "Runs directly on the hardware without a host OS (e.g., VMware ESXi, Microsoft Hyper-V, Xen).",
        "Type 2 Hypervisor (Hosted)": "Runs on a conventional operating system and manages VMs as applications (e.g., VMware Workstation, VirtualBox).",
        "Virtual Machines (VMs)": "A software emulation of a physical computer system, allowing multiple operating systems to run on the same hardware.",
        "Virtual Memory": "A system where the OS uses disk storage to extend RAM, allowing processes to use more memory than is physically available.",
        "Virtual Machine Monitor (VMM) / Hypervisor": "A software layer that manages virtual machines by mapping virtual resources to physical resources.",
        "VM Isolation": "The principle that each VM is independent and cannot directly interfere with others, improving security and reliability.",
        "VM Snapshots": "A saved state of a virtual machine that can be restored later.",
        "Write-Back Cache": "Writes data to memory only when the cache line is replaced.",
        "Write-Through Cache": "Writes data to both cache and main memory simultaneously."
    }
    
    # Create categories for terminology
    term_categories = {
        "Basic Virtualization Concepts": ["Virtual Machines (VMs)", "Virtual Machine Monitor (VMM) / Hypervisor", 
                                          "Type 1 Hypervisor (Bare Metal)", "Type 2 Hypervisor (Hosted)", 
                                          "Host OS vs. Guest OS", "VM Isolation", "VM Snapshots"],
        "Memory Virtualization": ["Virtual Memory", "Paging", "Page Table", "Page Fault", 
                                 "Memory Management Unit (MMU)", "Translation Lookaside Buffer (TLB)"],
        "CPU Virtualization": ["Hardware-Assisted Virtualization", "Trap-and-Emulate", 
                              "Full Virtualization", "Paravirtualization"],
        "Cache and Memory": ["Cache Coherence", "Snooping Protocol", "Write-Through Cache", 
                            "Write-Back Cache", "Resource Sharing", "Live Migration"]
    }

    # Sidebar enhancements
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>Learning Tools</h2>", unsafe_allow_html=True)
        
        # 1. Terminology explorer
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        st.markdown("<h3>Terminology Explorer</h3>", unsafe_allow_html=True)
        
        # Category selection first
        category = st.selectbox("Select Category", list(term_categories.keys()))
        
        # Then filter terms by category
        category_terms = term_categories[category]
        selected_term = st.selectbox("Select a Term", category_terms)
        
        st.markdown(f"<div class='definition-box'><p><b>{selected_term}:</b> {terminology[selected_term]}</p></div>", 
                  unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Quick Quiz Tool
        st.markdown("<div class='sidebar-content' style='margin-top: 2rem;'>", unsafe_allow_html=True)
        st.markdown("<h3>Test Your Knowledge</h3>", unsafe_allow_html=True)
        if st.button("Generate Quiz Question"):
            questions = [
                {"question": "Which hypervisor type runs directly on hardware?", 
                 "options": ["Type 1 (Bare Metal)", "Type 2 (Hosted)", "Paravirtualization", "Full Virtualization"],
                 "answer": "Type 1 (Bare Metal)"},
                {"question": "What does TLB stand for?", 
                 "options": ["Translation Language Buffer", "Translation Lookaside Buffer", "Transaction Lookaside Block", "Time Latency Bridge"],
                 "answer": "Translation Lookaside Buffer"},
                {"question": "Which of these is not a cache coherence mechanism?", 
                 "options": ["Snooping Protocol", "Directory-Based Coherence", "Memory Migration", "MESI Protocol"],
                 "answer": "Memory Migration"}
            ]
            random_q = np.random.choice(questions)
            st.session_state.current_q = random_q
            st.session_state.answered = False
            st.session_state.selected_answer = None
        
        if 'current_q' in st.session_state:
            st.write(st.session_state.current_q["question"])
            for option in st.session_state.current_q["options"]:
                if st.button(option, key=option):
                    st.session_state.selected_answer = option
                    st.session_state.answered = True
            
            if st.session_state.answered and st.session_state.selected_answer:
                if st.session_state.selected_answer == st.session_state.current_q["answer"]:
                    st.success("Correct! Well done.")
                else:
                    st.error(f"Incorrect. The right answer is: {st.session_state.current_q['answer']}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Main content area
    st.markdown("<h1 class='main-header'>Virtual Machines and Memory Virtualization</h1>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs(["Overview", "Virtual Machine Concepts", "Memory Virtualization", "Visualizations", "Resources"])
    
    with tabs[0]:
        st.markdown("<h2 class='section-header'>Abstract</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-content'>Virtualization is a powerful technology that enables multiple <span class='highlight-term'>Virtual Machines (VMs)</span> to run on a single physical system. This paper explores the fundamental concepts of virtual machines, memory virtualization, CPU instruction handling, and cache coherence. By leveraging <span class='highlight-term'>VM Isolation</span>, <span class='highlight-term'>Memory Virtualization</span>, <span class='highlight-term'>Cache Coherence</span>, and <span class='highlight-term'>Instruction Set Virtualization</span>, modern hypervisors optimize hardware utilization while ensuring robust performance.</p>", unsafe_allow_html=True)
        
        st.markdown("<h2 class='section-header'>Introduction</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-content'><span class='highlight-term'>Virtualization</span> enhances efficiency, security, and scalability in modern computing environments. Multiple <span class='highlight-term'>Virtual Machines (VMs)</span> run on a single system using a <span class='highlight-term'>Virtual Machine Monitor (VMM) / Hypervisor</span>, enabling efficient resource sharing and isolation. This paper discusses the various aspects of virtualization, including <span class='highlight-term'>virtual memory management</span>, <span class='highlight-term'>instruction set virtualization</span>, and <span class='highlight-term'>cache coherence</span> in multiprocessor systems.</p>", unsafe_allow_html=True)
        
        # Create an overview diagram
        st.markdown("<h3 class='subsection-header'>Virtualization Overview</h3>", unsafe_allow_html=True)
        
        # Display an overview image or diagram using Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#F0F2F6')
        ax.set_facecolor('#F0F2F6')
        
        # Create a simple diagram
        ax.add_patch(plt.Rectangle((0, 0), 10, 2, fc='#BFDBFE', ec='black', lw=2))
        ax.text(5, 1, 'Hardware (CPU, Memory, I/O)', ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Type 1
        ax.add_patch(plt.Rectangle((0, 2.5), 4.5, 1.5, fc='#93C5FD', ec='black', lw=2))
        ax.text(2.25, 3.25, 'Type 1 Hypervisor', ha='center', va='center', fontsize=11, fontweight='bold')
        
        ax.add_patch(plt.Rectangle((0.5, 4.5), 1, 1, fc='#DBEAFE', ec='black', lw=1))
        ax.text(1, 5, 'VM 1', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((2, 4.5), 1, 1, fc='#DBEAFE', ec='black', lw=1))
        ax.text(2.5, 5, 'VM 2', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((3.5, 4.5), 1, 1, fc='#DBEAFE', ec='black', lw=1))
        ax.text(4, 5, 'VM 3', ha='center', va='center', fontsize=10)
        
        # Type 2
        ax.add_patch(plt.Rectangle((5.5, 2.5), 4.5, 1.5, fc='#60A5FA', ec='black', lw=2))
        ax.text(7.75, 3.25, 'Host OS', ha='center', va='center', fontsize=11, fontweight='bold')
        
        ax.add_patch(plt.Rectangle((5.5, 4.5), 4.5, 1, fc='#93C5FD', ec='black', lw=1))
        ax.text(7.75, 5, 'Type 2 Hypervisor', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((6, 6), 1, 1, fc='#DBEAFE', ec='black', lw=1))
        ax.text(6.5, 6.5, 'VM 1', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((7.5, 6), 1, 1, fc='#DBEAFE', ec='black', lw=1))
        ax.text(8, 6.5, 'VM 2', ha='center', va='center', fontsize=10)
        
        # Add labels at the top
        ax.text(2.25, 7.2, 'Type 1 (Bare Metal)', ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(7.75, 7.2, 'Type 2 (Hosted)', ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Setting the limits and removing the axes
        ax.set_xlim(-0.5, 11)
        ax.set_ylim(-0.5, 8)
        ax.axis('off')
        
        st.pyplot(fig)
        
        st.markdown("<p class='text-content'>The diagram above illustrates the two primary hypervisor types. <span class='highlight-term'>Type 1 (Bare Metal)</span> hypervisors run directly on hardware, while <span class='highlight-term'>Type 2 (Hosted)</span> hypervisors run on a host operating system. Each approach has different performance characteristics and use cases.</p>", unsafe_allow_html=True)
        
    with tabs[1]:
        st.markdown("<h2 class='section-header'>Virtual Machine Operations</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-content'>A <span class='highlight-term'>Host OS vs. Guest OS</span> setup allows multiple <span class='highlight-term'>VMs</span> to operate within a single system. There are two primary types of hypervisors: <span class='highlight-term'>Type 1 Hypervisor (Bare Metal)</span>, which runs directly on hardware, and <span class='highlight-term'>Type 2 Hypervisor (Hosted)</span>, which runs within an existing operating system. <span class='highlight-term'>VM Snapshots</span> can save the state of a <span class='highlight-term'>VM</span> for later restoration, and <span class='highlight-term'>Live Migration</span> enables seamless movement between physical hosts.</p>", unsafe_allow_html=True)
        
        st.markdown("<h2 class='section-header'>CPU and Instruction Set Virtualization</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-content'><span class='highlight-term'>Trap-and-Emulate</span> is a technique used by the <span class='highlight-term'>VMM</span> to handle <span class='highlight-term'>Privileged Instructions</span> executed by a <span class='highlight-term'>Guest OS</span>. <span class='highlight-term'>Hardware-Assisted Virtualization</span> technologies, such as <span class='highlight-term'>Intel VT-x</span> and <span class='highlight-term'>AMD-V</span>, optimize performance and reduce emulation overhead. The <span class='highlight-term'>System Mode (Kernel Mode)</span> provides unrestricted hardware access, while <span class='highlight-term'>User Mode</span> restricts applications. <span class='highlight-term'>Trap Handling</span> ensures system security by switching execution to <span class='highlight-term'>System Mode</span> when needed.</p>", unsafe_allow_html=True)
        
        # Add comparison table
        st.markdown("<h3 class='subsection-header'>Comparison of Virtualization Approaches</h3>", unsafe_allow_html=True)
        
        comparison_data = {
            "Feature": ["Hardware Requirements", "Performance", "Isolation", "Guest OS Modification", "Common Use Cases"],
            "Full Virtualization": ["High", "Moderate", "Complete", "None", "Cloud Infrastructure, Testing Environments"],
            "Paravirtualization": ["Medium", "Good", "High", "Required", "Enterprise Servers, Cloud Hosting"],
            "Hardware-Assisted": ["VT-x/AMD-V", "Excellent", "Complete", "None", "Enterprise Virtualization, Cloud Computing"]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df.set_index("Feature"))
    
    with tabs[2]:
        st.markdown("<h2 class='section-header'>Memory Virtualization</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-content'><span class='highlight-term'>Virtual Memory</span> allows operating systems to extend <span class='highlight-term'>RAM</span> using disk storage. <span class='highlight-term'>Paging</span> divides <span class='highlight-term'>virtual memory</span> into fixed-size units, mapped by a <span class='highlight-term'>Page Table</span> and translated by the <span class='highlight-term'>Memory Management Unit (MMU)</span>. When a <span class='highlight-term'>Page Fault</span> occurs, the <span class='highlight-term'>OS</span> retrieves the missing page from disk. <span class='highlight-term'>Translation Lookaside Buffer (TLB)</span> caching optimizes memory access, reducing <span class='highlight-term'>TLB Miss</span> rates.</p>", unsafe_allow_html=True)
        
        st.markdown("<h3 class='subsection-header'>Memory Address Translation Process</h3>", unsafe_allow_html=True)
        
        # Create an interactive diagram for memory address translation
        # Using Matplotlib for a diagram
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#F0F2F6')
        ax.set_facecolor('#F0F2F6')
        
        # Virtual Address
        ax.add_patch(plt.Rectangle((1, 5), 6, 1, fc='#BFDBFE', ec='black', lw=2))
        ax.text(4, 5.5, 'Virtual Address', ha='center', va='center', fontsize=11, fontweight='bold')
        
        # Split into VPN and Offset
        ax.add_patch(plt.Rectangle((1, 4), 3, 1, fc='#93C5FD', ec='black', lw=2))
        ax.text(2.5, 4.5, 'Virtual Page Number', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((4, 4), 3, 1, fc='#60A5FA', ec='black', lw=2))
        ax.text(5.5, 4.5, 'Offset', ha='center', va='center', fontsize=10)
        
        # Arrows
        ax.arrow(2.5, 4, 0, -1, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(5.5, 4, 0, -1, head_width=0.2, head_length=0.2, fc='black', ec='black')
        
        # TLB and Page Table
        ax.add_patch(plt.Rectangle((1, 2), 3, 1, fc='#DBEAFE', ec='black', lw=2))
        ax.text(2.5, 2.5, 'TLB Lookup', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((5, 2), 3, 1, fc='#DBEAFE', ec='black', lw=2))
        ax.text(6.5, 2.5, 'Page Table', ha='center', va='center', fontsize=10)
        
        # Arrows down
        ax.arrow(2.5, 2, 0, -1, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(6.5, 2, 0, -1, head_width=0.2, head_length=0.2, fc='black', ec='black')
        
        # Physical frame number + offset
        ax.add_patch(plt.Rectangle((1, 0.5), 3, 1, fc='#93C5FD', ec='black', lw=2))
        ax.text(2.5, 1, 'Physical Frame Number', ha='center', va='center', fontsize=10)
        
        ax.add_patch(plt.Rectangle((4, 0.5), 3, 1, fc='#60A5FA', ec='black', lw=2))
        ax.text(5.5, 1, 'Offset', ha='center', va='center', fontsize=10)
        
        # Final arrow to physical address
        ax.arrow(4, 0.1, 0, -0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
        
        # Physical Address
        ax.add_patch(plt.Rectangle((1, -1), 6, 1, fc='#BFDBFE', ec='black', lw=2))
        ax.text(4, -0.5, 'Physical Address', ha='center', va='center', fontsize=11, fontweight='bold')
        
        # Connect TLB miss to page table
        ax.arrow(3.5, 2.5, 1, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')
        ax.text(4, 2.8, 'TLB Miss', color='red', ha='center', va='center', fontsize=9)
        
        # Setting the limits and removing the axes
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.5, 6.5)
        ax.axis('off')
        
        st.pyplot(fig)
        
        st.markdown("<p class='text-content'>The diagram illustrates the memory address translation process in virtualized environments. When a program accesses memory using a virtual address, it first checks the <span class='highlight-term'>TLB</span> for a quick translation. If not found (TLB miss), the system consults the <span class='highlight-term'>Page Table</span> for the mapping between virtual pages and physical frames. The offset portion remains unchanged throughout the translation.</p>", unsafe_allow_html=True)
        
        st.markdown("<h2 class='section-header'>Cache Coherence in Multiprocessor Systems</h2>", unsafe_allow_html=True)
        st.markdown("<p class='text-content'><span class='highlight-term'>Cache Coherence</span> ensures that multiple processors have a consistent view of <span class='highlight-term'>memory</span>. The <span class='highlight-term'>Snooping Protocol</span> monitors memory changes, while an <span class='highlight-term'>Invalidating Snooping Protocol</span> ensures consistency by removing outdated cache copies. <span class='highlight-term'>Directory-Based Coherence</span> scales better in large <span class='highlight-term'>multiprocessor</span> environments.</p>", unsafe_allow_html=True)
        
        st.markdown("<p class='text-content'><span class='highlight-term'>Write-Through Cache</span> writes data to both cache and main memory, while <span class='highlight-term'>Write-Back Cache</span> only writes to memory when necessary. <span class='highlight-term'>Cache Migration</span> moves frequently accessed data closer to the relevant <span class='highlight-term'>processor</span>. <span class='highlight-term'>Memory Consistency</span> defines rules for memory update visibility.</p>", unsafe_allow_html=True)
        
    with tabs[3]:
        st.markdown("<h2 class='section-header'>Interactive Visualizations</h2>", unsafe_allow_html=True)
        
        viz_type = st.selectbox("Select Visualization", 
                              ["VM Performance Comparison", "Memory Virtualization Overhead", "Cache Coherence Impact"])
        
        if viz_type == "VM Performance Comparison":
            # Sample data for VM performance
            vm_types = ["Bare Metal", "Type 1 Hypervisor", "Type 2 Hypervisor", "Container"]
            cpu_perf = [100, 95, 80, 98]
            io_perf = [100, 92, 75, 95]
            memory_perf = [100, 94, 85, 97]
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.arange(len(vm_types))
            width = 0.25
            
            ax.bar(x - width, cpu_perf, width, label='CPU Performance', color='#60A5FA')
            ax.bar(x, io_perf, width, label='I/O Performance', color='#93C5FD')
            ax.bar(x + width, memory_perf, width, label='Memory Performance', color='#BFDBFE')
            
            ax.set_title('Virtualization Performance Comparison (% of Bare Metal)', fontsize=14)
            ax.set_ylabel('Performance (%)', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(vm_types, fontsize=10)
            ax.set_ylim(0, 110)
            ax.legend()
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            st.pyplot(fig)
            
            st.markdown("<p class='text-content'>This chart compares the relative performance of different virtualization approaches. <span class='highlight-term'>Bare Metal</span> represents native hardware performance (100%). <span class='highlight-term'>Type 1 Hypervisors</span> achieve near-native performance, while <span class='highlight-term'>Type 2 Hypervisors</span> have more overhead due to the host OS layer. <span class='highlight-term'>Containers</span> offer lightweight virtualization with minimal performance impact.</p>", unsafe_allow_html=True)
            
        elif viz_type == "Memory Virtualization Overhead":
            # Create line chart for memory access latency
            page_sizes = [4, 8, 16, 32, 64, 128, 256]
            native_latency = [1, 1, 1, 1, 1, 1, 1]
            shadow_paging = [1.8, 1.65, 1.5, 1.4, 1.35, 1.3, 1.25]
            nested_paging = [1.4, 1.35, 1.3, 1.25, 1.2, 1.15, 1.1]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.plot(page_sizes, native_latency, 'o-', label='Native', linewidth=2, color='#2563EB')
            ax.plot(page_sizes, shadow_paging, 's-', label='Shadow Paging', linewidth=2, color='#60A5FA')
            ax.plot(page_sizes, nested_paging, '^-', label='Nested Paging (EPT/NPT)', linewidth=2, color='#93C5FD')
            
            ax.set_title('Memory Access Latency by Page Size', fontsize=14)
            ax.set_xlabel('Page Size (KB)', fontsize=12)
            ax.set_ylabel('Relative Latency (lower is better)', fontsize=12)
            ax.set_xscale('log', base=2)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            
            st.pyplot(fig)
            
            st.markdown("<p class='text-content'>This chart illustrates how different memory virtualization techniques affect access latency. <span class='highlight-term'>Shadow Paging</span>, used in software virtualization, incurs higher overhead compared to hardware-assisted <span class='highlight-term'>Nested Paging</span> technologies like Intel EPT or AMD NPT. Larger page sizes generally reduce virtualization overhead by requiring fewer translations.</p>", unsafe_allow_html=True)
            
        elif viz_type == "Cache Coherence Impact":
            # Create data for cache coherence impact
            processors = [1, 2, 4, 8, 16, 32, 64]
            bus_based = [1, 0.95, 0.85, 0.7, 0.5, 0.3, 0.2]
            directory_based = [1, 0.98, 0.95, 0.9, 0.85, 0.8, 0.75]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            ax.plot(processors, bus_based, 'o-', label='Bus-Based Snooping', linewidth=2, color='#60A5FA')
            ax.plot(processors, directory_based, 's-', label='Directory-Based Protocol', linewidth=2, color='#93C5FD')
            
            ax.set_title('Cache Coherence Scalability', fontsize=14)
            ax.set_xlabel('Number of Processors', fontsize=12)
            ax.set_ylabel('Relative Performance', fontsize=12)
            ax.set_xscale('log', base=2)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            
            st.pyplot(fig)
            
            st.markdown("<p class='text-content'>This visualization demonstrates how different <span class='highlight-term'>Cache Coherence</span> protocols scale with increasing processor counts. <span class='highlight-term'>Bus-Based Snooping</span> protocols perform well with few processors but don't scale to large systems due to bus bandwidth limitations. <span class='highlight-term'>Directory-Based</span> protocols maintain better performance as the system size increases, making them suitable for large-scale multiprocessor systems.</p>", unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("<h2 class='section-header'>Learning Resources</h2>", unsafe_allow_html=True)
        
        resource_tabs = st.tabs(["Videos", "Books & Papers", "Interactive Tools", "Courses"])
        
        with resource_tabs[0]:
            st.markdown("<h3 class='subsection-header'>Video Tutorials</h3>", unsafe_allow_html=True)
            
            video_resources = [
                {
                    "title": "Introduction to Virtual Machines",
                    "creator": "TechWorld with Nana",
                    "url": "https://www.youtube.com/watch?v=wX75Z-4MEoM",
                    "description": "A beginner-friendly introduction to virtual machines and their benefits",
                    "duration": "15:42"
                },
                {
                    "title": "Memory Virtualization Explained",
                    "creator": "Computer Science Center",
                    "url": "https://www.youtube.com/watch?v=dZqOlaDaBhY",
                    "description": "Technical explanation of how memory virtualization works in modern hypervisors",
                    "duration": "48:23"
                },
                {
                    "title": "Cache Coherence Protocols",
                    "creator": "MIT OpenCourseWare",
                    "url": "https://www.youtube.com/watch?v=rnGK12aQR6s",
                    "description": "Detailed lecture on MESI and other cache coherence protocols",
                    "duration": "52:10"
                }
            ]
            
            for video in video_resources:
                st.markdown(f"""
                <div style="padding: 1rem; margin-bottom: 1rem; border: 1px solid #E5E7EB; border-radius: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.2rem; color: #2563EB;">{video['title']}</h4>
                    <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>Creator:</strong> {video['creator']} | <strong>Duration:</strong> {video['duration']}</p>
                    <p style="margin: 0.5rem 0;">{video['description']}</p>
                    <a href="{video['url']}" target="_blank" style="color: #2563EB; text-decoration: none; font-weight: bold;">
                        Watch Video →
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        with resource_tabs[1]:
            st.markdown("<h3 class='subsection-header'>Books & Research Papers</h3>", unsafe_allow_html=True)
            
            book_resources = [
                {
                    "title": "A Primer on Memory Consistency and Cache Coherence",
                    "authors": "Daniel J. Sorin, Mark D. Hill, and David A. Wood",
                    "year": "2011",
                    "description": "Comprehensive reference on memory consistency models and cache coherence protocols",
                    "type": "Book"
                },
                {
                    "title": "Parallel Computer Architecture: A Hardware/Software Approach",
                    "authors": "David Culler and Jaswinder Pal Singh",
                    "year": "1999",
                    "description": "Foundational text covering parallel computing, including cache coherence and memory systems",
                    "type": "Book"
                },
                {
                    "title": "Memory Resource Management in VMware ESXi",
                    "authors": "Carl Waldspurger",
                    "year": "2002",
                    "description": "Classic paper describing memory management techniques in virtualized environments",
                    "type": "Research Paper"
                }
            ]
            
            for resource in book_resources:
                st.markdown(f"""
                <div style="padding: 1rem; margin-bottom: 1rem; border: 1px solid #E5E7EB; border-radius: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.2rem; color: #2563EB;">{resource['title']}</h4>
                    <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>Authors:</strong> {resource['authors']} | <strong>Year:</strong> {resource['year']} | <strong>Type:</strong> {resource['type']}</p>
                    <p style="margin: 0.5rem 0;">{resource['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with resource_tabs[2]:
            st.markdown("<h3 class='subsection-header'>Interactive Learning Tools</h3>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #BFDBFE; border-radius: 0.5rem; background-color: #EFF6FF;">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem; color: #2563EB;">Virtual Machine Simulator</h4>
                <p>Try this interactive simulator to explore how virtual machines manage resources:</p>
                
                <div style="margin: 1rem 0; padding: 1rem; background-color: white; border-radius: 0.5rem; border: 1px solid #DBEAFE;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <div style="font-weight: bold;">VM 1</div>
                        <div>
                            <label style="margin-right: 0.5rem;">Memory:</label>
                            <select>
                                <option>512 MB</option>
                                <option>1 GB</option>
                                <option>2 GB</option>
                                <option>4 GB</option>
                            </select>
                        </div>
                        <div>
                            <label style="margin-right: 0.5rem;">CPUs:</label>
                            <select>
                                <option>1</option>
                                <option>2</option>
                                <option>4</option>
                            </select>
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <div style="font-weight: bold;">VM 2</div>
                        <div>
                            <label style="margin-right: 0.5rem;">Memory:</label>
                            <select>
                                <option>512 MB</option>
                                <option>1 GB</option>
                                <option>2 GB</option>
                                <option>4 GB</option>
                            </select>
                        </div>
                        <div>
                            <label style="margin-right: 0.5rem;">CPUs:</label>
                            <select>
                                <option>1</option>
                                <option>2</option>
                                <option>4</option>
                            </select>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 1rem;">
                        <button style="background-color: #2563EB; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; cursor: pointer;">
                            Run Simulation
                        </button>
                    </div>
                </div>
                
                <p style="font-size: 0.9rem; margin-top: 1rem;">Note: This is a mock interface. In a real application, the simulator would show resource allocation and performance metrics.</p>
            </div>
            
            <div style="padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #BFDBFE; border-radius: 0.5rem; background-color: #EFF6FF;">
                <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem; color: #2563EB;">Memory Address Translator</h4>
                <p>Enter a virtual address to see how it translates to a physical address:</p>
                
                <div style="margin: 1rem 0; padding: 1rem; background-color: white; border-radius: 0.5rem; border: 1px solid #DBEAFE;">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <label style="margin-right: 0.5rem; font-weight: bold;">Virtual Address (hex):</label>
                        <input type="text" placeholder="0x12345678" style="padding: 0.5rem; border: 1px solid #D1D5DB; border-radius: 0.25rem;">
                        <button style="background-color: #2563EB; color: white; border: none; padding: 0.5rem 1rem; border-radius: 0.25rem; margin-left: 0.5rem; cursor: pointer;">
                            Translate
                        </button>
                    </div>
                    
                    <div style="background-color: #F9FAFB; padding: 1rem; border-radius: 0.25rem;">
                        <div style="margin-bottom: 0.5rem;"><strong>Page Number:</strong> <span>0x123</span></div>
                        <div style="margin-bottom: 0.5rem;"><strong>Offset:</strong> <span>0x45678</span></div>
                        <div style="margin-bottom: 0.5rem;"><strong>Physical Frame:</strong> <span>0xABC</span></div>
                        <div><strong>Physical Address:</strong> <span>0xABC45678</span></div>
                    </div>
                </div>
                
                <p style="font-size: 0.9rem; margin-top: 1rem;">Note: This is a mock interface. In a real application, the translator would perform actual calculations.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with resource_tabs[3]:
            st.markdown("<h3 class='subsection-header'>Online Courses</h3>", unsafe_allow_html=True)
            
            course_resources = [
                {
                    "title": "Cloud Computing Specialization",
                    "provider": "Coursera (University of Illinois)",
                    "url": "https://www.coursera.org/specializations/cloud-computing",
                    "description": "Comprehensive course series covering virtualization, cloud infrastructure, and distributed systems",
                    "level": "Intermediate"
                },
                {
                    "title": "Advanced Operating Systems",
                    "provider": "edX (Georgia Tech)",
                    "url": "https://www.edx.org/course/advanced-operating-systems",
                    "description": "Covers advanced OS concepts including memory management and virtualization technologies",
                    "level": "Advanced"
                },
                {
                    "title": "Virtualization for Beginners",
                    "provider": "Udemy",
                    "url": "https://www.udemy.com/course/virtualization-for-beginners",
                    "description": "Practical introduction to setting up and managing virtual machines with hands-on exercises",
                    "level": "Beginner"
                }
            ]
            
            for course in course_resources:
                st.markdown(f"""
                <div style="padding: 1rem; margin-bottom: 1rem; border: 1px solid #E5E7EB; border-radius: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.2rem; color: #2563EB;">{course['title']}</h4>
                    <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>Provider:</strong> {course['provider']} | <strong>Level:</strong> {course['level']}</p>
                    <p style="margin: 0.5rem 0;">{course['description']}</p>
                    <a href="{course['url']}" target="_blank" style="color: #2563EB; text-decoration: none; font-weight: bold;">
                        View Course →
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<h3 class='subsection-header'>References</h3>", unsafe_allow_html=True)
        st.markdown("<div class='references'>", unsafe_allow_html=True)
        st.markdown("""
        <ul>
            <li><strong>Intel VT-x and AMD-V documentation</strong> - <a href="https://www.intel.com/content/www/us/en/virtualization/virtualization-technology/intel-virtualization-technology.html" target="_blank">Intel</a></li>
            <li><strong>VMware ESXi official documentation</strong> - <a href="https://docs.vmware.com/en/VMware-vSphere/index.html" target="_blank">VMware</a></li>
            <li><strong>Microsoft Hyper-V documentation</strong> - <a href="https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview" target="_blank">Microsoft</a></li>
            <li><strong>Research paper on memory virtualization</strong> - <a href="https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-belay.pdf" target="_blank">USENIX</a></li>
            <li><strong>Cache Coherence for Modern Multicore Processors</strong> - <a href="https://scholar.google.com/scholar?q=Cache+Coherence+for+Modern+Multicore+Processors" target="_blank">Google Scholar</a></li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()