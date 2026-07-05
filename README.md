# StreamSniper Backend

FastAPI backend MVP for StreamSniper, a web app that helps clip creators find viral moments before everyone else.

## Install Dependencies

```bash
cd streamsniper-backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Run Locally

```bash
uvicorn app.main:app --reload
```

## Local Backend URL

```text
http://localhost:8000
```

## Swagger Docs URL

```text
http://localhost:8000/docs
```

## Example Fetch Calls

### GET /clips/trending

```js
const response = await fetch("http://localhost:8000/clips/trending");
const trendingClips = await response.json();
console.log(trendingClips);
```

### GET /creators

```js
const response = await fetch("http://localhost:8000/creators");
const creators = await response.json();
console.log(creators);
```

### POST /clips

```js
const response = await fetch("http://localhost:8000/clips", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    creator_id: 1,
    title: "New clip title",
    platform: "Twitch",
    url: "https://example.com/clips/new-clip",
    thumbnail_url: "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80",
    views: 150000,
    likes: 12000,
    comments: 900,
    posted_at: new Date().toISOString(),
  }),
});

const createdClip = await response.json();
console.log(createdClip);
```

## Endpoints

- `GET /`
- `POST /creators`
- `GET /creators`
- `GET /creators/{creator_id}`
- `DELETE /creators/{creator_id}`
- `POST /clips`
- `GET /clips`
- `GET /clips/trending`
- `GET /creators/{creator_id}/clips`
- `DELETE /clips/{clip_id}`

The app creates a local SQLite database named `streamsniper.db` and seeds demo creators and clips the first time it starts.
