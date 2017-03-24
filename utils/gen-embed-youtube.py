# youtube_url = 'http://youtu.be/tVAvp9a82TM'
# <iframe width="560" height="315" src="//www.youtube.com/embed/tVAvp9a82TM" frameborder="0" allowfullscreen></iframe>


youtube_url = 'https://youtu.be/DQTuHtmdfqk'


def create_html_for_youtube(video_url):
    the_html = """
    <p>You can watch the video below or view it on <a href="YOUTUBE_URL" target="_blank">You Tube</a>.</p>
    <p>
    EMBED
    </p>
    """

    # embed_str = '<iframe width="560" height="315" src="//www.youtube.com/embed/VIDEO_URL_HERE" frameborder="0" allowfullscreen></iframe>'
    # using responsive embed, tested on desktop, ipad and iphone
    embed_str = """
      <div class="responsive-embed-16by9-iframe-youtube">
        <div class="embed-responsive embed-responsive-16by9">
          <iframe class="embed-responsive-item" src="//www.youtube.com/embed/VIDEO_URL_HERE?rel=0" allowfullscreen></iframe>
        </div>
      </div>"""

    vurl = video_url.split('/')[3]
    embed_str = embed_str.replace('VIDEO_URL_HERE',vurl)
    the_html = the_html.replace('EMBED', embed_str).replace('YOUTUBE_URL',video_url)

    print the_html


create_html_for_youtube(youtube_url)

"""

SEE RESPONSIVE EMBED

http://getbootstrap.com/components/#panels
  <div class="embed-responsive embed-responsive-16by9">


  <div class="responsive-embed-16by9-iframe-youtube">
    <div class="embed-responsive embed-responsive-16by9">
      <iframe class="embed-responsive-item" src="//www.youtube.com/embed/VIDEO_URL_HERE?rel=0" allowfullscreen></iframe>
    </div>
  </div>


    <iframe width="560" height="315" src="//www.youtube.com/embed/x0t7tjbg7ks" frameborder="0" allowfullscreen></iframe>


  """