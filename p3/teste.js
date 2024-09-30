const getJSON = async(caminho) => {
    const resultado = await fetch(caminho);
    const dados = await resultado.json();
    return dados;
}

let vdados = getJSON("https://servicodados.ibge.gov.br/api/v1/localidades/municipios/3304557/distritos");


vdados.then(arr => {
    console.log(arr)
    })

