from django import template

register = template.Library()

def uppercase(string):
    return string.upper()

@register.filter(name='cleared')
def cleared(string):
    '''Escape space symbol | replace with '_' '''
    return string.replace(' ', '_')
    
def main():
    print(uppercase('hello wowrls'))
    print(cleared('hello wo wr l s'))

if __name__ == '__main__':
    main()