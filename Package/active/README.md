# Snake.exe download website

A responsive, single-page download site. No build tools or frameworks required.

## Add your Windows game

1. Put your compiled game executable in this folder:
   `downloads/snake-game.exe`
2. In `index.html`, find both download links and change:
   `data-ready` is not present by default. Add `data-ready="true"` to each of the two `<a>` elements whose `href` is `downloads/snake-game.exe`.
   Example:
   `<a class="btn btn-primary" href="downloads/snake-game.exe" download data-ready="true">`
3. Open `index.html` in your browser to test the design and download link.

If you prefer to distribute the EXE through GitHub Releases (recommended for larger files), upload the EXE as a release asset and replace both `href="downloads/snake-game.exe"` values with the direct asset URL. Then you can remove the small placeholder-warning script at the bottom of the page.

## Host it on GitHub Pages

1. Sign in to GitHub and create a new repository, for example `snake-game-site`.
2. Upload `index.html` and the `downloads` folder (with your EXE if you are using the local-file option) to the repository root. Keep `index.html` at the root.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Choose branch **main** and folder **/(root)**, then click **Save**.
6. Wait for GitHub Pages to finish publishing. Your website URL will look like:
   `https://YOUR-USERNAME.github.io/snake-game-site/`

## Important notes about EXE downloads

- GitHub Pages serves static website files; it does not run your game on the server.
- GitHub repositories have a 100 MB per-file limit for ordinary Git files. For a larger EXE, or for cleaner release management, use **GitHub Releases** and link to the uploaded release asset.
- Windows may show a SmartScreen or antivirus warning for a new/unsigned executable. Only distribute a build you created and tested, and give users an honest description of what it does.
- Test the download link after publishing. If the file is missing, check spelling and capitalization: `downloads/snake-game.exe`.
