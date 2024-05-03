
export class Scrapper {

  async getFullHtml(page: any){
    try {
      // return await page.evaluate(() => document.body.innerHTML);
      return await page.content();
    } catch (error) {
      return "error"
    }
  }

  async getResultElement(page: any): Promise<any>{}

  async getElement(page:any,selector:string){
    try {
      return await page.$(selector);
    } catch (error) {
      const url = page.url();
      await page.goto(url)
      await page.waitFor(5000)
      try {
        return await page.$(selector);
      } catch (error) {
        console.error(error)
        process.exit();
      }
    }
  }

  async getProposals(page: any): Promise<any>{}

  async getProposalAuthor(elementHandle: any): Promise<any>{}

  async getHomeProposals(page: any): Promise<any>{}

  async getChannelFilter(page: any): Promise<any>{}

  async getHomeChanels(page: any): Promise<any>{}

  async getHomeViews(page: any): Promise<any>{}

  async getHomeDate(page: any): Promise<any>{}

  async getHomeDuration(elementHandle: any): Promise<any>{}

  async getHomeTitles(page: any): Promise<any>{}


  async getHomeUrls(element:any): Promise<any>{}

  async getChannelTitle(page:any): Promise<any>{}

  async getTitle(page: any): Promise<any>{}

  async getAuthor(page: any): Promise<any>{}

  async fill(element:any, page: any): Promise<any>{}
}
