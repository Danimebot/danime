
def searchChar():
    query = '''
    query ($search: String) {
      Character(search: $search) {
        siteUrl
        name {
          full
        }
        media(perPage: 1) {
          nodes {
            title {
                romaji
                english
            }
            siteUrl
          }
        }
        image {
          large
        }
        description(asHtml: true)
      }
    }
    '''
    return query