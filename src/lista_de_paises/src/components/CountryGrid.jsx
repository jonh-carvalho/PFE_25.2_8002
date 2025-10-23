// src/components/CountryGrid.jsx
import CountryCard from './CountryCard';

function CountryGrid({ countries, favorites = [], onToggleFavorite }) {
  return (
    <div className="country-grid">
      {countries.map((country) => (
        <CountryCard 
          key={country.id}
          id={country.id}
          flag={country.flag}
          name={country.name}
          capital={country.capital}
          population={country.population}
          language={country.language}
          
          isFavorite={favorites.includes(country.id)}
          onToggleFavorite={onToggleFavorite}
        />
      ))}
    </div>
  );
}

export default CountryGrid;