# Linkr
Linkr is a file delivery system which downloads packages hosted on a web server.

## Working Principle
Linkr answers a simple question: "Instead of distributing files, why not host them on a web server and distribute a `linkr` file which can later be used to download the package?" This is the essence behind Linkr. Linkr has two functionalities:
- Creating `linkr` files
- Installing packages from `linkr` files

### Creating `linkr` files
To create a `linkr` attached to a given package, you need to host it somewhere. Suppose you want to create a `linkr` file for a directory `assets/`, then you will host the web server from the parent directory such that going to the web address `http://my-webserver.com/assets` takes you to the `assets` directory. From this parent directory, you will run **Linkr**, which will create an `assets.linkr` file in the same directory. Now, you can distribute this `linkr` file to others!

### Installing packages from `linkr` files
To install a package from a `linkr` file, you run **Linkr** in your desired location and input the `linkr` file. Linkr then starts downloading these files and will place them according to the desired directory structure.
