/**
 * Página de Contato (ContactPage)
 * Conteúdo estático
 */
function ContactPage() {
  return (
    <div className="bg-white p-6 sm:p-8 rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Página de Contato</h1>
      <div className="space-y-4 text-lg text-gray-700">
        <p>
          Entre em contato conosco através dos seguintes canais:
        </p>
        <ul className="list-disc list-inside space-y-2">
          <li>
            <strong>Email:</strong> <a href="mailto:contato@gestorprojetos.com" className="text-blue-600 hover:underline">contato@gestorprojetos.com</a>
          </li>
          <li>
            <strong>Telefone:</strong> (99) 99999-9999
          </li>
          <li>
            <strong>Endereço:</strong> Rua Fictícia, 123 - Centro
          </li>
        </ul>
      </div>
    </div>
  );
}

export default ContactPage;
