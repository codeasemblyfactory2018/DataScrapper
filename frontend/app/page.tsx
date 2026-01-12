import Link from 'next/link';

// Mock data for MVP display (until we connect backend)
const PRODUCTS = [
  {
    id: 1,
    name: "Dolina Noteci Premium (Bez Zboż)",
    producer: "Dolina Noteci",
    ranking: 1,
    image: "https://via.placeholder.com/150",
    prices: [
      { shop: "Ceneo", price: 8.50, url: "#" },
      { shop: "Allegro", price: 9.20, url: "#" },
    ]
  },
  {
    id: 2,
    name: "Wiejska Zagroda (Indyk z Jagnięciną)",
    producer: "Wiejska Zagroda",
    ranking: 2,
    image: "https://via.placeholder.com/150",
    prices: [
      { shop: "Ceneo", price: 12.00, url: "#" },
      { shop: "Zooplus", price: 11.50, url: "#" },
    ]
  }
];

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      {/* Header */}
      <header className="bg-emerald-600 text-white p-6 shadow-md">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold">🐱 Kocie Okazje</h1>
          <nav className="space-x-4">
            <Link href="#ranking" className="hover:underline">Ranking</Link>
            <Link href="#donate" className="hover:underline bg-white text-emerald-700 px-4 py-2 rounded-full font-bold transition">
              Wesprzyj Nas ❤️
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-emerald-700 text-white text-center py-12 px-4">
        <h2 className="text-4xl font-extrabold mb-4">Znajdź najzdrowszą karmę w najniższej cenie</h2>
        <p className="text-lg opacity-90 max-w-2xl mx-auto">
          Codziennie skanujemy sklepy, abyś nie przepłacał za zdrowie swojego pupila.
        </p>
      </section>

      {/* Main Ranking Table */}
      <main id="ranking" className="max-w-5xl mx-auto py-12 px-4">
        <h3 className="text-2xl font-bold mb-6 border-l-4 border-emerald-500 pl-4">Aktualny Ranking (Top 10)</h3>
        
        <div className="space-y-6">
          {PRODUCTS.map((product) => (
            <div key={product.id} className="bg-white rounded-xl shadow-sm hover:shadow-md transition border border-gray-100 p-6 flex flex-col md:flex-row gap-6">
              {/* Image & Rank */}
              <div className="relative w-full md:w-48 flex-shrink-0">
                <div className="absolute top-0 left-0 bg-emerald-500 text-white font-bold px-3 py-1 rounded-br-lg z-10">
                  #{product.ranking}
                </div>
                <div className="bg-gray-200 h-40 w-full rounded-lg flex items-center justify-center text-gray-500">
                  {/* Placeholder for real image */}
                  [Obrazek]
                </div>
              </div>

              {/* Details */}
              <div className="flex-1">
                <h4 className="text-xl font-bold text-gray-900 mb-1">{product.name}</h4>
                <p className="text-sm text-gray-500 mb-4">Producent: {product.producer}</p>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h5 className="text-sm font-semibold text-gray-600 mb-3">Najlepsze oferty dzisiaj:</h5>
                  <div className="space-y-2">
                    {product.prices.map((offer, idx) => (
                      <div key={idx} className="flex justify-between items-center border-b last:border-0 border-gray-200 pb-2 last:pb-0">
                        <span className="font-medium text-gray-700">{offer.shop}</span>
                        <div className="flex items-center gap-4">
                          <span className="font-bold text-emerald-600 text-lg">{offer.price.toFixed(2)} zł</span>
                          <a href={offer.url} className="text-sm text-emerald-600 hover:text-emerald-800 underline">
                            Idź do sklepu &rarr;
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Donation Section */}
      <section id="donate" className="bg-amber-50 py-12 border-t border-amber-100">
        <div className="max-w-3xl mx-auto text-center px-4">
          <h3 className="text-2xl font-bold text-amber-800 mb-4">Pomóż nam pomagać kotom 🐾</h3>
          <p className="text-amber-900 mb-8 leading-relaxed">
            Ten projekt jest utrzymywany pro bono. Twoja darowizna pozwala nam opłacać serwery i rozwijać nowe funkcje (jak bajki dla dzieci!).
          </p>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <button className="bg-amber-500 hover:bg-amber-600 text-white px-8 py-3 rounded-lg font-bold shadow-lg transition transform hover:-translate-y-1">
              Postaw Kawę ☕
            </button>
            <button className="bg-white border-2 border-amber-500 text-amber-600 px-8 py-3 rounded-lg font-bold hover:bg-amber-50 transition">
              Zgłoś prośbę / Kontakt
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-400 py-8 text-center text-sm">
        <p>&copy; 2026 Kocie Okazje. Wszystkie prawa zastrzeżone.</p>
      </footer>
    </div>
  );
}
