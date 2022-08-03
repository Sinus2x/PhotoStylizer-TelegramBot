import torch
import torchvision.transforms as tt
from torchvision.models import vgg19
from PIL import Image
from torch import nn
from PhotoStylizer.losses import gram_matrix, content_loss, style_loss


class StyleTransformer(nn.Module):

    def __init__(self, image_size=224):
        super().__init__()
        self.device = 'cpu'
        self.image_size = image_size
        self.content_layers = ['21']  # conv-4_2
        self.style_layers = ['0', '5', '10', '19', '28']  # conv1_1, conv2_1, conv3_1, conv4_1 and conv5_1
        self.chosen_layers = self.content_layers + self.style_layers
        self.n_content_layers = len(self.content_layers)
        self.n_style_layers = len(self.style_layers)
        self.vgg = vgg19(pretrained=True).features[:29].eval()  # vgg's feature extractor excluding layers after 28th
        self.cfg = {
            'epochs': 600,
            'lr': 0.01,
            'alpha': 1,
            'gamma': 100
        }
        # freeze the weights
        for m in self.vgg.children():
            m.requires_grad = False

        self.preprocess = tt.Compose(
            [
                tt.Resize((image_size, image_size)),
                tt.ToTensor()
            ]
        )

    def forward(self, x):
        content, style = [], []
        for name, layer in self.vgg.named_children():
            x = layer(x)

            if name in self.content_layers:
                content.append(x)

            elif name in self.style_layers:
                style.append(x)

        return content, style

    def transfer(self, inp, reference):
        w, h = Image.open(inp).size  # get original size
        inp = self.load_image(inp).unsqueeze(0).to(self.device)
        reference = self.load_image(reference).unsqueeze(0).to(self.device)

        init = torch.clone(inp).to(self.device)
        init.requires_grad = True
        opt = torch.optim.Adam([init], lr=self.cfg['lr'])

        inp_content, _ = self(inp)

        _, reference_style = self(reference)
        g_reference = []
        for feat in reference_style:
            g_reference.append(gram_matrix(feat))

        for epoch in range(self.cfg['epochs']):

            init_content, init_style = self(init)
            c_loss, s_loss = 0, 0

            # compute content loss
            for init_c, inp_c in zip(init_content, inp_content):
                c_loss += content_loss(inp_c.detach(), init_c)

            # compute style loss
            for init_s, g_ref in zip(init_style, g_reference):
                s_loss += style_loss(g_ref.detach(), init_s)

            loss = c_loss + self.cfg['gamma'] * s_loss

            opt.zero_grad()
            loss.backward()
            opt.step()

            # turn pixels into [0, 1] range to avoid noise
            with torch.no_grad():
                init.clamp_(0, 1)

            print(f'Epoch {epoch}: {c_loss, s_loss, loss}')

        return tt.ToPILImage()(
            tt.Resize((h, w))(
                init.squeeze(0).detach().cpu()
            )
        )

    def load_image(self, path):
        img = Image.open(path)
        img = self.preprocess(img)
        return img


