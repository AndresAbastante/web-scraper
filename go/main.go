package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/gocolly/colly"
)

type Product struct {
	Name  string
	Price string
	Url   string
}

func main() {

	scrapUrl := "https://listado.mercadolibre.com.ar/juegos-juguetes/juegos-mesa-cartas/cartas-coleccionables-rpg/pokemon_NoIndex_True_PublishedToday_YES_OrderId_PRICE"

	c := colly.NewCollector()

	c.SetRequestTimeout(120 * time.Second)

	products := make([]Product, 0)

	c.OnHTML("div.ui-search-result__wrapper", func(d *colly.HTMLElement) {
		d.ForEach("h2.ui-search-item__title", func(i int, h *colly.HTMLElement) {
			item := Product{}
			item.Name = h.Text
			item.Price = d.ChildText("span.price-tag-fraction")
			item.Url = d.ChildAttr("href", "ui-search-link")
			products = append(products, item)
		})

	})

	c.OnError(func(r *colly.Response, e error) {
		fmt.Println("Got this error:", e)
	})

	c.OnScraped(func(r *colly.Response) {
		fmt.Println("Finished", r.Request.URL)
		js, err := json.MarshalIndent(products, "", "    ")
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println("Writing data to file")
		if err := os.WriteFile("products.json", js, 0664); err == nil {
			fmt.Println("Data written to file successfully")
		}

	})

	c.Visit(scrapUrl)
}
