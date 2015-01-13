# youtube_url = 'http://youtu.be/tVAvp9a82TM'
# <iframe width="560" height="315" src="//www.youtube.com/embed/tVAvp9a82TM" frameborder="0" allowfullscreen></iframe>



youtube_url = 'http://youtu.be/tVAvp9a82TM'





def create_html_for_youtube(video_url):
    the_html = """
    <p>You can watch the video below or view it on <a href="YOUTUBE_URL" target="_blank">You Tube</a>.</p>
    <p>
    EMBED
    </p>
    """
    embed_str = '<iframe width="560" height="315" src="//www.youtube.com/embed/VIDEO_URL_HERE" frameborder="0" allowfullscreen></iframe>'
    vurl = video_url.split('/')[3]
    embed_str = embed_str.replace('VIDEO_URL_HERE',vurl)
    the_html = the_html.replace('EMBED', embed_str).replace('YOUTUBE_URL',video_url)

    print the_html


create_html_for_youtube(youtube_url)


