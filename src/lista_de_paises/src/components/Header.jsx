// src/components/Header.jsx
function Header({ title, subtitle, favoriteCount  }) {
  return (
    <header className="app-header">
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}

      <div className="favorite-counter">
        <span>❤️ {favoriteCount} países favoritos</span>
      </div>

    </header>
  );
}
export default Header;