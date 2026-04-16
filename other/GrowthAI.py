import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MultiURLSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GA4 Multi-URL Traffic Generator - Random Journey")
        self.geometry("1200x800")
        
        self.is_running = False
        self.visit_count = 0
        self.drivers = []
        self.url_list = []
        
        # Header
        header = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color="#1a5f3d")
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(header, text="🌐 Multi-URL Journey Simulator", 
                    font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)
        
        # Main Content
        main = ctk.CTkFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # URL List Section
        url_section = ctk.CTkFrame(main)
        url_section.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(url_section, text="📝 Paste Your URLs (One per line):", 
                    font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(url_section, text="Example:\nhttps://yoursite.com/\nhttps://yoursite.com/about\nhttps://yoursite.com/blog/post-1", 
                    text_color="gray", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=2)
        
        self.url_text = scrolledtext.ScrolledText(url_section, height=8, bg="#1a1a1a", fg="white", 
                                                  font=("Consolas", 11), wrap="word")
        self.url_text.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Quick add buttons
        quick_frame = ctk.CTkFrame(url_section, fg_color="transparent")
        quick_frame.pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkButton(quick_frame, text="📋 Load URLs", command=self.load_urls, 
                     width=120, height=30).pack(side="left", padx=5)
        ctk.CTkButton(quick_frame, text="🗑️ Clear", command=lambda: self.url_text.delete(1.0, "end"), 
                     width=120, height=30, fg_color="gray").pack(side="left", padx=5)
        
        self.url_count_label = ctk.CTkLabel(quick_frame, text="URLs loaded: 0", 
                                           font=ctk.CTkFont(size=12))
        self.url_count_label.pack(side="left", padx=20)
        
        # Settings
        settings_frame = ctk.CTkFrame(main)
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        # Row 1
        row1 = ctk.CTkFrame(settings_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row1, text="👥 Concurrent Users:").pack(side="left", padx=10)
        self.concurrent_entry = ctk.CTkEntry(row1, width=80)
        self.concurrent_entry.insert(0, "3")
        self.concurrent_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="🔄 Total Sessions:").pack(side="left", padx=10)
        self.sessions_entry = ctk.CTkEntry(row1, width=80)
        self.sessions_entry.insert(0, "10")
        self.sessions_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(row1, text="📄 Pages per Session:").pack(side="left", padx=10)
        self.pages_entry = ctk.CTkEntry(row1, width=80)
        self.pages_entry.insert(0, "5")
        self.pages_entry.pack(side="left", padx=5)
        
        # Row 2
        row2 = ctk.CTkFrame(settings_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        ctk.CTkLabel(row2, text="⏱️ Time per Page (sec):").pack(side="left", padx=10)
        self.time_min = ctk.CTkEntry(row2, width=60, placeholder_text="Min")
        self.time_min.insert(0, "15")
        self.time_min.pack(side="left", padx=2)
        
        ctk.CTkLabel(row2, text="-").pack(side="left")
        
        self.time_max = ctk.CTkEntry(row2, width=60, placeholder_text="Max")
        self.time_max.insert(0, "45")
        self.time_max.pack(side="left", padx=2)
        
        # Journey Mode
        ctk.CTkLabel(row2, text="🎯 Journey Mode:").pack(side="left", padx=20)
        self.journey_var = ctk.StringVar(value="random")
        ctk.CTkRadioButton(row2, text="Random", variable=self.journey_var, 
                          value="random").pack(side="left", padx=5)
        ctk.CTkRadioButton(row2, text="Sequential", variable=self.journey_var, 
                          value="sequential").pack(side="left", padx=5)
        
        # Behavior Options
        behavior_frame = ctk.CTkFrame(main)
        behavior_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(behavior_frame, text="🎬 Realistic Behaviors:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        behaviors = ctk.CTkFrame(behavior_frame, fg_color="transparent")
        behaviors.pack(anchor="w", padx=30, pady=5)
        
        self.scroll_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(behaviors, text="📜 Scroll", variable=self.scroll_var).pack(side="left", padx=10)
        
        self.mouse_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(behaviors, text="🖱️ Mouse Move", variable=self.mouse_var).pack(side="left", padx=10)
        
        self.click_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(behaviors, text="👆 Click Elements", variable=self.click_var).pack(side="left", padx=10)
        
        self.typing_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(behaviors, text="⌨️ Type in Inputs", variable=self.typing_var).pack(side="left", padx=10)
        
        # Traffic Source
        source_frame = ctk.CTkFrame(main)
        source_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(source_frame, text="🔗 Traffic Source:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.source_var = ctk.StringVar(value="google")
        sources_container = ctk.CTkFrame(source_frame, fg_color="transparent")
        sources_container.pack(anchor="w", padx=30, pady=5)
        
        sources = [
            ("Google", "google"), ("Facebook", "facebook"), ("Twitter", "twitter"),
            ("Pinterest", "pinterest"), ("Reddit", "reddit"), ("Direct", "direct")
        ]
        
        for text, value in sources:
            ctk.CTkRadioButton(sources_container, text=text, variable=self.source_var, 
                              value=value).pack(side="left", padx=8)
        
        # Control Buttons
        button_frame = ctk.CTkFrame(main)
        button_frame.pack(pady=15)
        
        self.start_btn = ctk.CTkButton(button_frame, text="🚀 START SIMULATION", 
                                       command=self.start_simulation, width=300, height=440,
                                       fg_color="#2a9d5f", hover_color="#1f7a47",
                                       font=ctk.CTkFont(size=16, weight="bold"))
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = ctk.CTkButton(button_frame, text="⏹ STOP ALL", 
                                      command=self.stop_simulation, width=300, height=50,
                                      fg_color="#d32f2f", hover_color="#a82222",
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      state="disabled")
        self.stop_btn.pack(side="left", padx=10)
        
        # Stats
        stats_frame = ctk.CTkFrame(main)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        self.stats_label = ctk.CTkLabel(stats_frame, 
                                       text="Active: 0 | Total Sessions: 0 | Pages Viewed: 0", 
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.stats_label.pack(pady=10)
        
        self.progress = ctk.CTkProgressBar(stats_frame, width=800, height=20)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Log
        ctk.CTkLabel(main, text="📊 Activity Log:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=5)
        self.log_text = scrolledtext.ScrolledText(main, height=8, bg="#0d1117", fg="#58a6ff", 
                                                  font=("Consolas", 10), wrap="word")
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Footer
        footer = ctk.CTkLabel(main, 
                             text="⚠️ Educational Tool - Use only on YOUR websites with GA4 installed", 
                             text_color="#ff9800", font=ctk.CTkFont(size=11))
        footer.pack(pady=10)

    def log(self, message, color=None):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.update_idletasks()

    def load_urls(self):
        """Extract and validate URLs from text box"""
        text = self.url_text.get(1.0, "end").strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please paste some URLs first!")
            return
        
        # Extract URLs using regex
        url_pattern = re.compile(r'https?://[^\s]+')
        urls = url_pattern.findall(text)
        
        # Clean and validate
        self.url_list = []
        for url in urls:
            url = url.strip().rstrip('.,;')
            if url:
                self.url_list.append(url)
        
        if not self.url_list:
            messagebox.showerror("Error", "No valid URLs found!\nMake sure URLs start with http:// or https://")
            return
        
        self.url_count_label.configure(text=f"URLs loaded: {len(self.url_list)}")
        self.log(f"✅ Loaded {len(self.url_list)} URLs")
        
        # Show first few URLs
        for i, url in enumerate(self.url_list[:3]):
            self.log(f"   {i+1}. {url}")
        if len(self.url_list) > 3:
            self.log(f"   ... and {len(self.url_list)-3} more")

    def start_simulation(self):
        # Load URLs first
        self.load_urls()
        
        if len(self.url_list) == 0:
            messagebox.showerror("Error", "No URLs to visit! Please add URLs first.")
            return
        
        try:
            concurrent = int(self.concurrent_entry.get())
            sessions = int(self.sessions_entry.get())
            pages_per_session = int(self.pages_entry.get())
            time_min = int(self.time_min.get())
            time_max = int(self.time_max.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return
        
        if concurrent > 10:
            messagebox.showwarning("Warning", "Max 10 concurrent users recommended!")
            return
        
        if time_max < time_min:
            messagebox.showerror("Error", "Max time must be greater than min time!")
            return
        
        self.is_running = True
        self.visit_count = 0
        self.page_views = 0
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.set(0)
        
        self.log("="*70)
        self.log("🚀 MULTI-URL JOURNEY SIMULATION STARTED")
        self.log(f"🎯 URLs in rotation: {len(self.url_list)}")
        self.log(f"👥 Concurrent users: {concurrent}")
        self.log(f"🔄 Total sessions: {sessions}")
        self.log(f"📄 Pages per session: {pages_per_session}")
        self.log(f"⏱️ Time per page: {time_min}-{time_max}s")
        self.log(f"🎯 Journey mode: {self.journey_var.get()}")
        self.log(f"🔗 Traffic source: {self.source_var.get()}")
        self.log("="*70)
        
        thread = threading.Thread(target=self.run_simulation, 
                                 args=(concurrent, sessions, pages_per_session, time_min, time_max))
        thread.daemon = True
        thread.start()

    def stop_simulation(self):
        self.is_running = False
        self.log("⏹ Stopping all sessions...")
        
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass
        self.drivers.clear()
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.update_stats()
        self.log("✅ All sessions terminated")

    def run_simulation(self, concurrent, sessions, pages_per_session, time_min, time_max):
        threads = []
        sessions_per_thread = sessions // concurrent
        
        for i in range(concurrent):
            thread = threading.Thread(target=self.simulate_user_journey, 
                                     args=(sessions_per_thread, pages_per_session, 
                                           time_min, time_max, i+1))
            thread.daemon = True
            threads.append(thread)
            thread.start()
            time.sleep(random.uniform(1, 3))
        
        for thread in threads:
            thread.join()
        
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.log("="*70)
        self.log(f"✅ SIMULATION COMPLETE!")
        self.log(f"📊 Total Sessions: {self.visit_count}")
        self.log(f"📄 Total Page Views: {self.page_views}")
        self.log(f"🎯 Check GA4 Real-Time Reports Now!")
        self.log("="*70)

    def simulate_user_journey(self, sessions, pages_per_session, time_min, time_max, user_id):
        for session_num in range(sessions):
            if not self.is_running:
                break
            
            driver = None
            try:
                # Setup browser
                options = uc.ChromeOptions()
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument(f'--user-agent={self.get_random_user_agent()}')
                
                referrer = self.get_referrer()
                if referrer:
                    options.add_argument(f'--referrer={referrer}')
                
                driver = uc.Chrome(options=options, version_main=None)
                self.drivers.append(driver)
                
                # Random screen size
                sizes = [(1920,1080), (1366,768), (1440,900), (1536,864), (1280,720)]
                w, h = random.choice(sizes)
                driver.set_window_size(w, h)
                
                self.visit_count += 1
                self.log(f"👤 User #{user_id} | Session #{session_num+1} - Starting journey")
                
                # Create journey path
                if self.journey_var.get() == "random":
                    journey = random.sample(self.url_list, min(pages_per_session, len(self.url_list)))
                else:
                    journey = self.url_list[:pages_per_session]
                
                # Visit each page in journey
                for page_num, url in enumerate(journey, 1):
                    if not self.is_running:
                        break
                    
                    try:
                        self.log(f"   📄 User #{user_id} | Page {page_num}/{len(journey)}: {url[:60]}...")
                        driver.get(url)
                        time.sleep(random.uniform(2, 4))
                        
                        self.page_views += 1
                        self.update_stats()
                        
                        # Time on page
                        time_on_page = random.uniform(time_min, time_max)
                        start_time = time.time()
                        
                        # Realistic behaviors
                        while time.time() - start_time < time_on_page:
                            if not self.is_running:
                                break
                            
                            if self.scroll_var.get() and random.random() < 0.8:
                                self.smooth_scroll(driver)
                            
                            if self.mouse_var.get() and random.random() < 0.5:
                                self.random_mouse(driver)
                            
                            if self.click_var.get() and random.random() < 0.3:
                                self.click_random_element(driver)
                            
                            if self.typing_var.get() and random.random() < 0.2:
                                self.type_in_search(driver)
                            
                            time.sleep(random.uniform(1, 3))
                        
                        actual_time = int(time.time() - start_time)
                        self.log(f"   ✓ User #{user_id} | Spent {actual_time}s on page")
                        
                    except Exception as e:
                        self.log(f"   ⚠️ User #{user_id} | Error on page: {str(e)[:40]}")
                
                self.log(f"🏁 User #{user_id} | Session complete ({len(journey)} pages)")
                
            except Exception as e:
                self.log(f"❌ User #{user_id} | Session error: {str(e)[:50]}")
            
            finally:
                if driver:
                    try:
                        driver.quit()
                        self.drivers.remove(driver)
                    except:
                        pass
                
                self.update_stats()
                
                if session_num < sessions - 1 and self.is_running:
                    wait = random.uniform(15, 30)
                    self.log(f"⏸️ User #{user_id} | Break for {int(wait)}s")
                    time.sleep(wait)

    def smooth_scroll(self, driver):
        """Realistic scrolling"""
        try:
            total = driver.execute_script("return document.body.scrollHeight")
            viewport = driver.execute_script("return window.innerHeight")
            
            for _ in range(random.randint(3, 8)):
                pos = random.randint(0, max(0, total - viewport))
                driver.execute_script(f"window.scrollTo({{top: {pos}, behavior: 'smooth'}});")
                time.sleep(random.uniform(0.5, 2))
        except:
            pass

    def random_mouse(self, driver):
        """Random mouse movement"""
        try:
            actions = ActionChains(driver)
            for _ in range(random.randint(2, 5)):
                x = random.randint(-200, 200)
                y = random.randint(-200, 200)
                actions.move_by_offset(x, y).perform()
                time.sleep(random.uniform(0.3, 0.8))
        except:
            pass

    def click_random_element(self, driver):
        """Click random clickable element"""
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "button, a, input[type='submit']")
            if elements:
                elem = random.choice(elements[:10])
                driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                time.sleep(0.5)
                elem.click()
                time.sleep(random.uniform(1, 2))
        except:
            pass

    def type_in_search(self, driver):
        """Type in search/input fields"""
        try:
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='search']")
            if inputs:
                inp = random.choice(inputs)
                driver.execute_script("arguments[0].scrollIntoView(true);", inp)
                time.sleep(0.5)
                inp.click()
                
                words = ["test", "search", "hello", "example", "query"]
                text = random.choice(words)
                
                for char in text:
                    inp.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
        except:
            pass

    def update_stats(self):
        """Update statistics display"""
        active = len(self.drivers)
        self.stats_label.configure(
            text=f"Active: {active} | Total Sessions: {self.visit_count} | Pages Viewed: {self.page_views}"
        )

    def get_referrer(self):
        """Get referrer based on traffic source"""
        sources = {
            "google": "https://www.google.com/search?q=your+keywords",
            "facebook": "https://www.facebook.com/",
            "twitter": "https://twitter.com/",
            "pinterest": "https://www.pinterest.com/",
            "reddit": "https://www.reddit.com/",
            "direct": None
        }
        return sources.get(self.source_var.get())

    def get_random_user_agent(self):
        """Random user agents"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        ]
        return random.choice(agents)


if __name__ == "__main__":
    app = MultiURLSimulator()
    app.mainloop()