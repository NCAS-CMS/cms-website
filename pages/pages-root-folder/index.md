---
#
# Use the widgets beneath and the content will be inserted automagically in the webpage.
# To make this work, you have to use › layout: frontpage
#
layout: frontpage
#header:
#  image_fullwidth: header_unsplash_12.jpg
widget1:
  title: "User Support"
  url: '/user-support/'
  image: widget-1-302x182.jpg
  text: 'CMS provides user support to the UK atmospheric and polar science community:<br/>1. Helpdesk<br/>2. FAQs<br/>3. Documentation'
widget2:
  title: "Services"
  url: '/services/'
  text: 'CMS provides HPC resource management, training and software engineering support for the UK atmospheric and polar science community.'
  video: '<a href="#" data-reveal-id="videoModal"><img src="http://phlow.github.io/feeling-responsive/images/start-video-feeling-responsive-302x182.jpg" width="302" height="182" alt=""/></a>'
widget3:
  title: "Infrastructure"
  url: '/infrastructure/'
  image: widget-github-303x182.jpg
  text: 'CMS provides the infrastructure to allow users to run various complex modelling workflows (e.g. UM, NEMO, etc) on national platforms.<br/>1. PUMA<br/>2. Rose/Cylc & FCM<br/>3. Data transfer<br/>4. Tools & Utilities'
#
# Use the call for action to show a button on the frontpage
#
# To make internal links, just use a permalink like this
# url: /getting-started/
#
# To style the button in different colors, use no value
# to use the main color or success, alert or secondary.
# To change colors see sass/_01_settings_colors.scss
#
#callforaction:
#  url: https://tinyletter.com/feeling-responsive
#  text: Inform me about new updates and features ›
#  style: alert
#
# This is a nasty hack to make the navigation highlight
# this page as active in the topbar navigation
#
homepage: true
permalink: /index.html
---

<div id="videoModal" class="reveal-modal large" data-reveal="">
  <div class="flex-video widescreen vimeo" style="display: block;">
    <iframe width="1280" height="720" src="https://www.youtube.com/embed/3b5zCFSmVvU" frameborder="0" allowfullscreen></iframe>
  </div>
  <a class="close-reveal-modal">&#215;</a>
</div>
