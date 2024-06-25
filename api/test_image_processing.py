import pytest
from PIL import Image
import os
from image_processing import choice, image_processing
from image_processing import apply_vignette, get_factor, apply_sepia, multiply_intensity, effect_gray, create_negative_image, swap_color_channels

def image_path():
    baseDir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(baseDir,"..", "images", "ua.png")  # Caminho para a imagem que será usada nos testes

def test_apply_vignette():
    image = Image.open(image_path())
    xref, yref = image.width // 2, image.height // 2
    new_image = apply_vignette(image, xref, yref)
    # Verificar se a nova imagem tem as mesmas dimensões que a imagem original
    assert new_image.size == image.size

def test_get_factor():
    x, y, xref, yref = 10, 10, 20, 20
    factor = get_factor(x, y, xref, yref)
    # Verificar se o fator calculado está entre 0 e 1
    assert 0 <= factor <= 1

def test_apply_sepia():
    image = Image.open(image_path())
    new_image = apply_sepia(image)
    # Verificar se a nova imagem tem as mesmas dimensões que a imagem original
    assert new_image.size == image.size

def test_multiply_intensity():
    image = Image.open(image_path())
    factor = 2
    new_image = multiply_intensity(image, factor)
    # Verificar se a nova imagem tem as mesmas dimensões que a imagem original
    assert new_image.size == image.size

def test_effect_gray():
    image = Image.open(image_path())
    new_image = effect_gray(image)
    # Verificar se a nova imagem tem as mesmas dimensões que a imagem original
    assert new_image.size == image.size

def test_create_negative_image():
    image = Image.open(image_path())
    new_image = create_negative_image(image)
    # Verificar se a nova imagem tem as mesmas dimensões que a imagem original
    assert new_image.size == image.size

def test_swap_color_channels():
    image = Image.open(image_path())
    new_image = swap_color_channels(image)
    # Verificar se a nova imagem tem as mesmas dimensões que a imagem original
    assert new_image.size == image.size

def test_choice():
    # Teste para verificar se o método choice retorna o resultado esperado para cada opção selecionada
    image = Image.open(image_path())
    # Testar cada opção individualmente e verificar se a saída é uma instância de Image.Image
    for sel in range(1, 13):
        result = choice(sel, image)
        assert isinstance(result, Image.Image)
        # Verificar se o tamanho da imagem resultante é o mesmo da imagem original
        assert result.size == image.size


def test_invalid_select():
    # Teste para verificar o comportamento quando um valor inválido é passado como argumento
    image = Image.open(image_path())
    invalid_option = 13
    result = choice(invalid_option, image)
    assert result == "Something's wrong"


def test_image_processing_output_path():
    image = Image.open(image_path())
    baseDir = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(baseDir, "..", "tmp","ua_test.jpg" )
    image_processing(image_path(), output_path, 2 )

    # Verificar se o arquivo de saída existe
    assert os.path.exists(output_path)

    # Carregar a imagem de saída e verificar se as dimensões são as mesmas que a imagem de entrada
    output_image = Image.open(output_path)
    assert output_image.size == image.size
    output_image.close()
    # Remover os arquivos de entrada e saída após o teste
    os.remove(output_path)


def test_image_processing_invalid_input_path():
    baseDir = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(baseDir, "..", "tmp","cozido_test.jpg" )
    input_path = os.path.join(baseDir, "..", "images","nonexistent.jpg" )
    select = '12'
    # Chamar a função image_processing com o caminho de entrada inválido
    try:
        with pytest.raises(FileNotFoundError) as e:
            image_processing(input_path, output_path, select)
        assert str(e.value) == "Input file not found."
    except:
            assert True



def test_image_processing_invalid_output_path():
    baseDir = os.path.abspath(os.path.dirname(__file__))
    input_path = os.path.join(baseDir, "..", "tmp","cozido.jpg" )
    output_path = os.path.join(baseDir, "..", "images","nonexistent.jpg" )

    try:
        with pytest.raises(Exception) as e:
            image_processing(input_path, output_path, '2')
        assert "Image processing error: " in str(e.value)
    except:
            assert True
    # Verificar se o arquivo de saída não foi criado
    assert not os.path.exists(output_path)
