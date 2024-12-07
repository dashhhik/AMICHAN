export default function Cont() {
  const handleLoginClickGETCODE = () => {
    console.log("Hyi");
    window.location.href = "auth/"
  }
  const handleLoginAUTH = () => {
    window.location.href = "vk.com"
  }
    return (
      <>
  <div className="container">
  <header className="header">
    <h1 className="title">Amichan</h1>
    <img className="log" src="https://www.hse.ru/mirror/pubs/share/522215913" width={75}></img>
    <button onClick={handleLoginClickGETCODE}>Получить Код</button>
    <button onClick={handleLoginAUTH}>Авторизация</button>
  </header>

  <main className="main">
    <h2 className="welcome">Добро пожаловать. Снова.</h2>
    <div className="table-container">
      <table className="links-table">
        <thead>
          <tr>
            <th>Название</th>
            <th>Описание</th>
            <th>Ссылка</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>SrachThread</td>
            <td>Дальше Бога нет.</td>
            <td>
              <a href="https://www.google.com">
                https://www.google.com
              </a>
            </td>
          </tr>
          <tr>
            <td>Zalupa Ivanicha</td>
            <td>щфщвфщвщфвщфвщф</td>
            <td>
              <a href="https://www.youtube.com">
                https://www.youtube.com
              </a>
            </td>
          </tr>
          <tr>
            <td>Видеоигры</td>
            <td>Я мейню Абрамса в Дедлокиче</td>
            <td>
              <a href="https://www.github.com">
                https://www.github.com
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</div>
      </>
    );
  }
