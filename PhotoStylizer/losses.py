import torch


def content_loss(target_content: torch.Tensor,
                 input_content: torch.Tensor) -> torch.Tensor:
    """

    target_content: 1 x C x H x W, given style-image
    input_style: 1 x C x H x W, generated image

    returns: content loss of the given layer
    """
    loss = 0.5 * torch.mean(torch.square(input_content - target_content))
    return loss


def gram_matrix(input_tensor: torch.Tensor) -> torch.Tensor:
    """
    input_tensor: 1 x C x H x W

    returns: gram_matrix of the given layer
    """
    channels = input_tensor.shape[1]
    a = input_tensor.view(channels, -1)

    # norm ?
    return torch.matmul(a, a.t())


def style_loss(reference_gram: torch.Tensor,
               input_style: torch.Tensor) -> torch.Tensor:
    """
    reference_gram: gram-matrix of the layer's output
    input_style: 1 x C x H x W, generated image

    returns: style loss of the given layer
    """
    g_input = gram_matrix(input_style)

    loss = 0.5 * torch.mean(torch.square(g_input - reference_gram))
    return loss
