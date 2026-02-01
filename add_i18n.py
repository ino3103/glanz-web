#!/usr/bin/env python3
"""
Comprehensive script to add data-i18n attributes to GLANZ landing page HTML
"""

import re

# Read the HTML file
with open('/Users/apple/Projects/glamz/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define all replacements (pattern -> replacement with data-i18n)
replacements = [
    # Navigation
    (r'(<a href="#home" class="nav-link")>Home</a>', r'\1 data-i18n="nav_home">Home</a>'),
    (r'(<a href="#about" class="nav-link")>About</a>', r'\1 data-i18n="nav_about">About</a>'),
    (r'(<a href="#products" class="nav-link")>Products</a>', r'\1 data-i18n="nav_products">Products</a>'),
    (r'(<a href="#benefits" class="nav-link")>Benefits</a>', r'\1 data-i18n="nav_benefits">Benefits</a>'),
    (r'(<a href="#bundles" class="nav-link")>Bundles</a>', r'\1 data-i18n="nav_bundles">Bundles</a>'),
    (r'(<a href="#contact" class="nav-link")>Contact</a>', r'\1 data-i18n="nav_contact">Contact</a>'),
    
    # Hero Section
    (r'(<div class="hero-badge")>Premium Hair Care</div>', r'\1 data-i18n="hero_badge">Premium Hair Care</div>'),
    (r'(<span class="hero-title-line")>Unlock Your</span>', r'\1 data-i18n="hero_title_1">Unlock Your</span>'),
    (r'(<span class="hero-title-line accent")>Natural Radiance</span>', r'\1 data-i18n="hero_title_2">Natural Radiance</span>'),
    (r'(<p class="hero-subtitle")>Experience the luxury.*?</p>', r'\1 data-i18n="hero_subtitle">Experience the luxury of professional hair care with GLANZ Wellness Hub. Our scientifically formulated products nourish, repair, and transform your hair from within.</p>'),
    (r'(<a href="#products" class="btn btn-primary")>Explore Products</a>', r'\1 data-i18n="hero_btn_primary">Explore Products</a>'),
    (r'(<a href="#bundles" class="btn btn-secondary")>View Bundles</a>', r'\1 data-i18n="hero_btn_secondary">View Bundles</a>'),
    (r'<span>Scroll to discover</span>', r'<span data-i18n="hero_scroll">Scroll to discover</span>'),
    
    # About Section
    (r'(<div class="section-label")>About GLANZ</div>', r'\1 data-i18n="about_label">About GLANZ</div>'),
    (r'<h2 class="section-title">Where Science Meets <span class="accent">Luxury</span></h2>', r'<h2 class="section-title"><span data-i18n="about_title_1">Where Science Meets</span> <span class="accent" data-i18n="about_title_2">Luxury</span></h2>'),
    (r'(<p class="about-text")>GLANZ Wellness Hub was born.*?</p>', r'\1 data-i18n="about_text_1">GLANZ Wellness Hub was born from a passion for transforming hair care into a luxurious ritual. Our products combine cutting-edge hair science with premium natural ingredients to deliver visible results you can feel.</p>'),
    (r'(<p class="about-text")>Every bottle is crafted.*?</p>', r'\1 data-i18n="about_text_2">Every bottle is crafted with care, designed to address specific hair concerns while providing an indulgent sensory experience. From anti-hair loss solutions to deep keratin repair, we\'ve got your hair journey covered.</p>'),
    (r'(<span class="stat-number")>500ml</span>', r'\1 data-i18n="about_stat_1_number">500ml</span>'),
    (r'(<span class="stat-label")>Premium Formulas</span>', r'\1 data-i18n="about_stat_1_label">Premium Formulas</span>'),
    (r'(<span class="stat-number")>100%</span>', r'\1 data-i18n="about_stat_2_number">100%</span>'),
    (r'(<span class="stat-label")>Satisfaction Focused</span>', r'\1 data-i18n="about_stat_2_label">Satisfaction Focused</span>'),
    (r'(<span class="stat-number")>3\+</span>', r'\1 data-i18n="about_stat_3_number">3+</span>'),
    (r'(<span class="stat-label")>Targeted Solutions</span>', r'\1 data-i18n="about_stat_3_label">Targeted Solutions</span>'),
    
    # Products Section Headers
    (r'(<div class="section-label")>Our Collection</div>', r'\1 data-i18n="products_label">Our Collection</div>'),
    (r'<h2 class="section-title">Premium Hair Care <span class="accent">Products</span></h2>', r'<h2 class="section-title"><span data-i18n="products_title_1">Premium Hair Care</span> <span class="accent" data-i18n="products_title_2">Products</span></h2>'),
    (r'(<p class="section-subtitle")>Discover our carefully curated.*?</p>', r'\1 data-i18n="products_subtitle">Discover our carefully curated range of professional-grade hair care solutions</p>'),
    
    # Product 1
    (r'(<span class="product-tag")>Best Seller</span>', r'\1 data-i18n="product_1_tag">Best Seller</span>', 1),
    (r'(<h3 class="product-title")>Hair Loss Nourishing Shampoo</h3>', r'\1 data-i18n="product_1_title">Hair Loss Nourishing Shampoo</h3>', 1),
    (r'(<p class="product-description")>Anti-frizz formula designed.*?</p>', r'\1 data-i18n="product_1_desc">Anti-frizz formula designed to promote hair growth and repair damaged strands. Enriched with nourishing ingredients for stronger, healthier hair.</p>', 1),
    (r'(<span class="product-size")>500ml</span>', r'\1 data-i18n="product_1_size">500ml</span>', 1),
    (r'(<a href="#" class="product-link")>Learn More →</a>', r'\1 data-i18n="product_1_link">Learn More →</a>', 1),
    
    # Product 2
    (r'(<span class="product-tag")>Deep Treatment</span>', r'\1 data-i18n="product_2_tag">Deep Treatment</span>'),
    (r'(<h3 class="product-title")>Keratin Repair Hair Mask</h3>', r'\1 data-i18n="product_2_title">Keratin Repair Hair Mask</h3>'),
    (r'(<p class="product-description")>Intensive rejuvenation treatment.*?</p>', r'\1 data-i18n="product_2_desc">Intensive rejuvenation treatment for ultimate smoothness. Restores damaged hair with deep keratin infusion for silky, manageable locks.</p>', 1),
    
    # Product 3
    (r'(<span class="product-tag")>Premium Oil</span>', r'\1 data-i18n="product_3_tag">Premium Oil</span>'),
    (r'(<h3 class="product-title")>Hair Therapy Oil</h3>', r'\1 data-i18n="product_3_title">Hair Therapy Oil</h3>'),
    (r'(<p class="product-description")>Luxurious therapy oil.*?</p>', r'\1 data-i18n="product_3_desc">Luxurious therapy oil that restores and promotes hair growth. Lightweight formula absorbs quickly, leaving hair nourished without greasiness.</p>', 1),
    (r'(<span class="product-size")>250ml</span>', r'\1 data-i18n="product_3_size">250ml</span>', 1),
    
    # Product 4
    (r'(<span class="product-tag")>Accessory</span>', r'\1 data-i18n="product_4_tag">Accessory</span>'),
    (r'(<h3 class="product-title")>Silicone Scalp Massager</h3>', r'\1 data-i18n="product_4_title">Silicone Scalp Massager</h3>'),
    (r'(<p class="product-description")>Ergonomic scalp massager.*?</p>', r'\1 data-i18n="product_4_desc">Ergonomic scalp massager designed to stimulate blood circulation and enhance product absorption. Available in elegant neutral tones.</p>', 1),
    (r'(<span class="product-size")>3 Colors</span>', r'\1 data-i18n="product_4_size">3 Colors</span>'),
    
    # Benefits Section
    (r'(<div class="section-label")>Why Choose GLANZ</div>', r'\1 data-i18n="benefits_label">Why Choose GLANZ</div>'),
    (r'<h2 class="section-title">Experience the <span class="accent">Difference</span></h2>', r'<h2 class="section-title"><span data-i18n="benefits_title_1">Experience the</span> <span class="accent" data-i18n="benefits_title_2">Difference</span></h2>'),
    (r'(<h3 class="benefit-title")>Premium Quality</h3>', r'\1 data-i18n="benefit_1_title">Premium Quality</h3>'),
    (r'(<p class="benefit-text")>Every product is formulated.*?</p>', r'\1 data-i18n="benefit_1_text">Every product is formulated with the finest ingredients, ensuring exceptional quality and visible results.</p>', 1),
    (r'(<h3 class="benefit-title")>Gentle Formulas</h3>', r'\1 data-i18n="benefit_2_title">Gentle Formulas</h3>'),
    (r'(<p class="benefit-text")>Carefully balanced formulas.*?</p>', r'\1 data-i18n="benefit_2_text">Carefully balanced formulas that are gentle on your hair and scalp while delivering powerful results.</p>', 1),
    (r'(<h3 class="benefit-title")>Scientifically Proven</h3>', r'\1 data-i18n="benefit_3_title">Scientifically Proven</h3>'),
    (r'(<p class="benefit-text")>Backed by research.*?</p>', r'\1 data-i18n="benefit_3_text">Backed by research and developed with advanced hair science to target specific concerns effectively.</p>', 1),
    (r'(<h3 class="benefit-title")>Long-Lasting Results</h3>', r'\1 data-i18n="benefit_4_title">Long-Lasting Results</h3>'),
    (r'(<p class="benefit-text")>Experience transformative results.*?</p>', r'\1 data-i18n="benefit_4_text">Experience transformative results that last, with consistent use revealing healthier, more vibrant hair.</p>', 1),
    
    # Gallery Section
    (r'(<div class="section-label")>Gallery</div>', r'\1 data-i18n="gallery_label">Gallery</div>'),
    (r'<h2 class="section-title">See Our Products in <span class="accent">Action</span></h2>', r'<h2 class="section-title"><span data-i18n="gallery_title_1">See Our Products in</span> <span class="accent" data-i18n="gallery_title_2">Action</span></h2>'),
    
    # Bundles Section
    (r'(<div class="section-label")>Complete Solutions</div>', r'\1 data-i18n="bundles_label">Complete Solutions</div>'),
    (r'<h2 class="section-title">Curated Hair Care <span class="accent">Bundles</span></h2>', r'<h2 class="section-title"><span data-i18n="bundles_title_1">Curated Hair Care</span> <span class="accent" data-i18n="bundles_title_2">Bundles</span></h2>'),
    (r'(<p class="section-subtitle")>Get the complete GLANZ experience.*?</p>', r'\1 data-i18n="bundles_subtitle">Get the complete GLANZ experience with our specially curated bundles</p>'),
    
    # Bundle 1
    (r'(<span class="bundle-tag")>Starter Set</span>', r'\1 data-i18n="bundle_1_tag">Starter Set</span>', 1),
    (r'(<h3 class="bundle-title")>The Essential Duo</h3>', r'\1 data-i18n="bundle_1_title">The Essential Duo</h3>', 1),
    (r'(<p class="bundle-description")>Perfect for beginners.*?</p>', r'\1 data-i18n="bundle_1_desc">Perfect for beginners. Includes our Hair Loss Nourishing Shampoo and Keratin Repair Hair Mask for a complete cleansing and treatment routine.</p>', 1),
    (r'<li>Hair Loss Nourishing Shampoo \(500ml\)</li>', r'<li data-i18n="bundle_1_item_1">Hair Loss Nourishing Shampoo (500ml)</li>', 1),
    (r'<li>Keratin Repair Hair Mask \(500ml\)</li>', r'<li data-i18n="bundle_1_item_2">Keratin Repair Hair Mask (500ml)</li>', 1),
    (r'(<a href="#" class="btn btn-primary")>Shop Bundle</a>', r'\1 data-i18n="bundle_1_btn">Shop Bundle</a>', 1),
    
    # Bundle 2
    (r'(<div class="bundle-badge")>Most Popular</div>', r'\1 data-i18n="bundle_2_badge">Most Popular</div>'),
    (r'(<span class="bundle-tag")>Complete Care</span>', r'\1 data-i18n="bundle_2_tag">Complete Care</span>', 1),
    (r'(<h3 class="bundle-title")>The Ultimate Trio</h3>', r'\1 data-i18n="bundle_2_title">The Ultimate Trio</h3>', 1),
    (r'(<p class="bundle-description")>Our most popular bundle.*?</p>', r'\1 data-i18n="bundle_2_desc">Our most popular bundle. Complete your hair care ritual with all three core products plus two bonus scalp massagers for enhanced results.</p>', 1),
    (r'<li>2x Silicone Scalp Massagers</li>', r'<li data-i18n="bundle_2_item_4">2x Silicone Scalp Massagers</li>'),
    
    # Bundle 3
    (r'(<span class="bundle-tag")>Treatment Focus</span>', r'\1 data-i18n="bundle_3_tag">Treatment Focus</span>', 1),
    (r'(<h3 class="bundle-title")>Intensive Therapy Pack</h3>', r'\1 data-i18n="bundle_3_title">Intensive Therapy Pack</h3>'),
    (r'(<p class="bundle-description")>For those who need intensive treatment.*?</p>', r'\1 data-i18n="bundle_3_desc">For those who need intensive treatment. Multiple bottles of our signature Hair Therapy Oil for extended treatment periods or to share with loved ones.</p>', 1),
    (r'<li>5x Hair Therapy Oil \(250ml each\)</li>', r'<li data-i18n="bundle_3_item_1">5x Hair Therapy Oil (250ml each)</li>'),
    (r'<li>Free Scalp Massager</li>', r'<li data-i18n="bundle_3_item_2">Free Scalp Massager</li>'),
    
    # Testimonials Section
    (r'(<div class="section-label")>Testimonials</div>', r'\1 data-i18n="testimonials_label">Testimonials</div>'),
    (r'<h2 class="section-title">What Our Customers <span class="accent">Say</span></h2>', r'<h2 class="section-title"><span data-i18n="testimonials_title_1">What Our Customers</span> <span class="accent" data-i18n="testimonials_title_2">Say</span></h2>'),
    (r'(<p class="testimonial-text")>"After just two weeks.*?</p>', r'\1 data-i18n="testimonial_1_text">"After just two weeks of using the Hair Therapy Oil, I noticed significantly less hair fall. The quality is unlike anything I\'ve tried before. Truly premium!"</p>', 1),
    (r'(<span class="author-name")>Sarah M\.</span>', r'\1 data-i18n="testimonial_1_name">Sarah M.</span>', 1),
    (r'(<span class="author-title")>Verified Buyer</span>', r'\1 data-i18n="testimonial_1_title">Verified Buyer</span>', 1),
    (r'(<p class="testimonial-text")>"The Keratin Hair Mask.*?</p>', r'\1 data-i18n="testimonial_2_text">"The Keratin Hair Mask transformed my damaged hair completely. It\'s so soft and manageable now. I\'ve recommended GLANZ to all my friends!"</p>', 1),
    (r'(<span class="author-name")>Amina K\.</span>', r'\1 data-i18n="testimonial_2_name">Amina K.</span>'),
    (r'(<span class="author-title")>Verified Buyer</span>', r'\1 data-i18n="testimonial_2_title">Verified Buyer</span>', 2),
    (r'(<p class="testimonial-text")>"The entire product line.*?</p>', r'\1 data-i18n="testimonial_3_text">"The entire product line feels so luxurious. From the elegant packaging to the amazing scent, every detail shows quality. My hair has never looked better!"</p>', 1),
    (r'(<span class="author-name")>John D\.</span>', r'\1 data-i18n="testimonial_3_name">John D.</span>'),
    (r'(<span class="author-title")>Verified Buyer</span>', r'\1 data-i18n="testimonial_3_title">Verified Buyer</span>', 3),
    
    # CTA Section
    (r'(<h2 class="cta-title")>Ready to Transform Your Hair\?</h2>', r'\1 data-i18n="cta_title">Ready to Transform Your Hair?</h2>'),
    (r'(<p class="cta-text")>Join thousands of satisfied.*?</p>', r'\1 data-i18n="cta_text">Join thousands of satisfied customers who have discovered the GLANZ difference. Start your journey to healthier, more beautiful hair today.</p>'),
    (r'(<a href="#products" class="btn btn-primary btn-large")>Shop Now</a>', r'\1 data-i18n="cta_btn_primary">Shop Now</a>'),
    (r'(<a href="#contact" class="btn btn-secondary btn-large")>Contact Us</a>', r'\1 data-i18n="cta_btn_secondary">Contact Us</a>'),
    
    # Contact Section
    (r'(<div class="section-label")>Get in Touch</div>', r'\1 data-i18n="contact_label">Get in Touch</div>'),
    (r'<h2 class="section-title">We\'d Love to <span class="accent">Hear from You</span></h2>', r'<h2 class="section-title"><span data-i18n="contact_title_1">We\'d Love to</span> <span class="accent" data-i18n="contact_title_2">Hear from You</span></h2>'),
    (r'(<p class="contact-text")>Have questions about our products.*?</p>', r'\1 data-i18n="contact_text">Have questions about our products or need personalized recommendations? Our team is here to help you find the perfect hair care solution.</p>'),
    (r'(<label for="name")>Full Name</label>', r'\1 data-i18n="form_name_label">Full Name</label>'),
    (r'<input type="text" id="name" name="name" placeholder="Enter your name"', r'<input type="text" id="name" name="name" data-i18n-placeholder="form_name_placeholder" placeholder="Enter your name"'),
    (r'(<label for="email")>Email Address</label>', r'\1 data-i18n="form_email_label">Email Address</label>'),
    (r'<input type="email" id="email" name="email" placeholder="Enter your email"', r'<input type="email" id="email" name="email" data-i18n-placeholder="form_email_placeholder" placeholder="Enter your email"'),
    (r'(<label for="subject")>Subject</label>', r'\1 data-i18n="form_subject_label">Subject</label>'),
    (r'<input type="text" id="subject" name="subject" placeholder="How can we help\?"', r'<input type="text" id="subject" name="subject" data-i18n-placeholder="form_subject_placeholder" placeholder="How can we help?"'),
    (r'(<label for="message")>Message</label>', r'\1 data-i18n="form_message_label">Message</label>'),
    (r'<textarea id="message" name="message" rows="5" placeholder="Tell us more\.\.\."', r'<textarea id="message" name="message" rows="5" data-i18n-placeholder="form_message_placeholder" placeholder="Tell us more..."'),
    (r'(<button type="submit" class="btn btn-primary btn-full")>Send Message</button>', r'\1 data-i18n="form_submit">Send Message</button>'),
    
    # Footer
    (r'(<p class="footer-tagline")>Premium hair care solutions.*?</p>', r'\1 data-i18n="footer_tagline">Premium hair care solutions for your wellness journey.</p>'),
    (r'<h4>Quick Links</h4>', r'<h4 data-i18n="footer_quick_links">Quick Links</h4>', 1),
    (r'<h4>Products</h4>', r'<h4 data-i18n="footer_products">Products</h4>'),
    (r'<h4>Support</h4>', r'<h4 data-i18n="footer_support">Support</h4>'),
    (r'<a href="#">Hair Loss Shampoo</a>', r'<a href="#" data-i18n="footer_product_1">Hair Loss Shampoo</a>'),
    (r'<a href="#">Keratin Hair Mask</a>', r'<a href="#" data-i18n="footer_product_2">Keratin Hair Mask</a>'),
    (r'<a href="#">Hair Therapy Oil</a>', r'<a href="#" data-i18n="footer_product_3">Hair Therapy Oil</a>'),
    (r'<a href="#">Scalp Massager</a>', r'<a href="#" data-i18n="footer_product_4">Scalp Massager</a>'),
    (r'<a href="#">FAQ</a>', r'<a href="#" data-i18n="footer_support_1">FAQ</a>'),
    (r'<a href="#">Shipping Info</a>', r'<a href="#" data-i18n="footer_support_2">Shipping Info</a>'),
    (r'<a href="#">Returns</a>', r'<a href="#" data-i18n="footer_support_3">Returns</a>'),
    (r'<a href="#">Privacy Policy</a>', r'<a href="#" data-i18n="footer_support_4">Privacy Policy</a>'),
    (r'<p>&copy; 2026 GLANZ Wellness Hub\. All rights reserved\.</p>', r'<p data-i18n="footer_copyright">&copy; 2026 GLANZ Wellness Hub. All rights reserved.</p>'),
]

# Apply all replacements
for pattern, replacement, *count in replacements:
    if count:
        html = re.sub(pattern, replacement, html, count=count[0], flags=re.DOTALL)
    else:
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Write the updated HTML
with open('/Users/apple/Projects/glamz/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Successfully added data-i18n attributes to all translatable content!")
print("The landing page now supports English and Swahili language switching.")
