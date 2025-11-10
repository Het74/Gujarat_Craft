from django import template

register = template.Library()


@register.filter
def youtube_embed_url(url):
    """Convert YouTube or Vimeo URL to embed URL"""
    if not url:
        return ''
    
    # YouTube URL handling
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtube.com/embed/' in url:
        return url
    
    # Vimeo URL handling
    elif 'vimeo.com/' in url:
        if '/video/' in url:
            video_id = url.split('/video/')[1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        elif '/player.vimeo.com/video/' in url:
            return url
        else:
            # Extract video ID from vimeo.com/XXXXX format
            video_id = url.split('vimeo.com/')[1].split('?')[0].split('/')[0]
            return f'https://player.vimeo.com/video/{video_id}'
    
    # Return URL as-is for other embeddable URLs
    return url


@register.filter
def user_initials(user):
    """Get user initials for avatar display"""
    if not user or not user.username:
        return 'U'
    
    username = user.username.strip().upper()
    if len(username) >= 2:
        return username[0] + username[1]
    elif len(username) == 1:
        return username[0] + username[0]
    else:
        return 'U'
