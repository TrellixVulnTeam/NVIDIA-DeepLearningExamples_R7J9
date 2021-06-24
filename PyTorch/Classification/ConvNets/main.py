# Copyright (c) 2018-2019, NVIDIA CORPORATION
# Copyright (c) 2017-      Facebook, Inc
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import argparse
<<<<<<< HEAD
import os
import shutil
import time
import random

import numpy as np
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
=======
import random
from copy import deepcopy
import signal

import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.nn.parallel
>>>>>>> repo1
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
<<<<<<< HEAD

# try:
#     from apex.parallel import DistributedDataParallel as DDP
#     from apex.fp16_utils import *
#     from apex import amp
# except ImportError:
#     raise ImportError(
#         "Please install apex from https://www.github.com/nvidia/apex to run this example."
#     )

import image_classification.resnet as models
=======
from torch.nn.parallel import DistributedDataParallel as DDP

>>>>>>> repo1
import image_classification.logger as log

from image_classification.smoothing import LabelSmoothing
from image_classification.mixup import NLLMultiLabelSmooth, MixUpWrapper
from image_classification.dataloaders import *
from image_classification.training import *
from image_classification.utils import *
<<<<<<< HEAD

import dllogger


def add_parser_arguments(parser):
    model_names = models.resnet_versions.keys()
    model_configs = models.resnet_configs.keys()

=======
from image_classification.models import (
    resnet50,
    resnext101_32x4d,
    se_resnext101_32x4d,
    efficientnet_b0,
    efficientnet_b4,
    efficientnet_widese_b0,
    efficientnet_widese_b4,
)
import dllogger


def available_models():
    models = {
        m.name: m
        for m in [
            resnet50,
            resnext101_32x4d,
            se_resnext101_32x4d,
            efficientnet_b0,
            efficientnet_b4,
            efficientnet_widese_b0,
            efficientnet_widese_b4,
        ]
    }
    return models


def add_parser_arguments(parser, skip_arch=False):
>>>>>>> repo1
    parser.add_argument("data", metavar="DIR", help="path to dataset")
    parser.add_argument(
        "--data-backend",
        metavar="BACKEND",
        default="dali-cpu",
        choices=DATA_BACKEND_CHOICES,
        help="data backend: "
        + " | ".join(DATA_BACKEND_CHOICES)
        + " (default: dali-cpu)",
    )
<<<<<<< HEAD

    parser.add_argument(
        "--arch",
        "-a",
        metavar="ARCH",
        default="resnet50",
        choices=model_names,
        help="model architecture: " + " | ".join(model_names) + " (default: resnet50)",
    )

    parser.add_argument(
        "--model-config",
        "-c",
        metavar="CONF",
        default="classic",
        choices=model_configs,
        help="model configs: " + " | ".join(model_configs) + "(default: classic)",
    )

    parser.add_argument(
        "--num-classes",
        metavar="N",
        default=1000,
        type=int,
        help="number of classes in the dataset",
    )
=======
    parser.add_argument(
        "--interpolation",
        metavar="INTERPOLATION",
        default="bilinear",
        help="interpolation type for resizing images: bilinear, bicubic or triangular(DALI only)",
    )
    if not skip_arch:
        model_names = available_models().keys()
        parser.add_argument(
            "--arch",
            "-a",
            metavar="ARCH",
            default="resnet50",
            choices=model_names,
            help="model architecture: " + " | ".join(model_names) + " (default: resnet50)",
        )
>>>>>>> repo1

    parser.add_argument(
        "-j",
        "--workers",
        default=5,
        type=int,
        metavar="N",
        help="number of data loading workers (default: 5)",
    )
    parser.add_argument(
        "--epochs",
<<<<<<< HEAD
        default=1,
=======
        default=90,
>>>>>>> repo1
        type=int,
        metavar="N",
        help="number of total epochs to run",
    )
    parser.add_argument(
        "--run-epochs",
        default=-1,
        type=int,
        metavar="N",
        help="run only N epochs, used for checkpointing runs",
    )
    parser.add_argument(
<<<<<<< HEAD
        "-b",
        "--batch-size",
        default=128,
=======
        "--early-stopping-patience",
        default=-1,
        type=int,
        metavar="N",
        help="early stopping after N epochs without validation accuracy improving",
    )
    parser.add_argument(
        "--image-size", default=None, type=int, help="resolution of image"
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        default=256,
>>>>>>> repo1
        type=int,
        metavar="N",
        help="mini-batch size (default: 256) per gpu",
    )

    parser.add_argument(
        "--optimizer-batch-size",
        default=-1,
        type=int,
        metavar="N",
        help="size of a total batch size, for simulating bigger batches using gradient accumulation",
    )

    parser.add_argument(
        "--lr",
        "--learning-rate",
        default=0.1,
        type=float,
        metavar="LR",
        help="initial learning rate",
    )
    parser.add_argument(
        "--lr-schedule",
<<<<<<< HEAD
        default="cosine",
=======
        default="step",
>>>>>>> repo1
        type=str,
        metavar="SCHEDULE",
        choices=["step", "linear", "cosine"],
        help="Type of LR schedule: {}, {}, {}".format("step", "linear", "cosine"),
    )

<<<<<<< HEAD
=======
    parser.add_argument("--end-lr", default=0, type=float)

>>>>>>> repo1
    parser.add_argument(
        "--warmup", default=0, type=int, metavar="E", help="number of warmup epochs"
    )

    parser.add_argument(
        "--label-smoothing",
<<<<<<< HEAD
        default=0.1,
=======
        default=0.0,
>>>>>>> repo1
        type=float,
        metavar="S",
        help="label smoothing",
    )
    parser.add_argument(
        "--mixup", default=0.0, type=float, metavar="ALPHA", help="mixup alpha"
    )
<<<<<<< HEAD
=======
    parser.add_argument(
        "--optimizer", default="sgd", type=str, choices=("sgd", "rmsprop")
    )
>>>>>>> repo1

    parser.add_argument(
        "--momentum", default=0.9, type=float, metavar="M", help="momentum"
    )
    parser.add_argument(
        "--weight-decay",
        "--wd",
        default=1e-4,
        type=float,
        metavar="W",
        help="weight decay (default: 1e-4)",
    )
    parser.add_argument(
        "--bn-weight-decay",
        action="store_true",
        help="use weight_decay on batch normalization learnable parameters, (default: false)",
    )
    parser.add_argument(
<<<<<<< HEAD
=======
        "--rmsprop-alpha",
        default=0.9,
        type=float,
        help="value of alpha parameter in rmsprop optimizer (default: 0.9)",
    )
    parser.add_argument(
        "--rmsprop-eps",
        default=1e-3,
        type=float,
        help="value of eps parameter in rmsprop optimizer (default: 1e-3)",
    )

    parser.add_argument(
>>>>>>> repo1
        "--nesterov",
        action="store_true",
        help="use nesterov momentum, (default: false)",
    )

    parser.add_argument(
        "--print-freq",
        "-p",
        default=10,
        type=int,
        metavar="N",
        help="print frequency (default: 10)",
    )
    parser.add_argument(
        "--resume",
        default=None,
        type=str,
        metavar="PATH",
        help="path to latest checkpoint (default: none)",
    )
    parser.add_argument(
<<<<<<< HEAD
        "--pretrained-weights",
        default="",
        type=str,
        metavar="PATH",
        help="load weights from here",
    )

    parser.add_argument("--fp16", action="store_true", help="Run model fp16 mode.")
    parser.add_argument(
        "--static-loss-scale",
        type=float,
        default=1,
        help="Static loss scale, positive power of 2 values can improve fp16 convergence.",
=======
        "--static-loss-scale",
        type=float,
        default=1,
        help="Static loss scale, positive power of 2 values can improve amp convergence.",
>>>>>>> repo1
    )
    parser.add_argument(
        "--dynamic-loss-scale",
        action="store_true",
        help="Use dynamic loss scaling.  If supplied, this argument supersedes "
        + "--static-loss-scale.",
    )
    parser.add_argument(
        "--prof", type=int, default=-1, metavar="N", help="Run only N iterations"
    )
    parser.add_argument(
        "--amp",
        action="store_true",
        help="Run model AMP (automatic mixed precision) mode.",
    )

    parser.add_argument(
        "--seed", default=None, type=int, help="random seed used for numpy and pytorch"
    )

    parser.add_argument(
        "--gather-checkpoints",
        action="store_true",
        help="Gather checkpoints throughout the training, without this flag only best and last checkpoints will be stored",
    )

    parser.add_argument(
        "--raport-file",
        default="experiment_raport.json",
        type=str,
        help="file in which to store JSON experiment raport",
    )

    parser.add_argument(
        "--evaluate", action="store_true", help="evaluate checkpoint/model"
    )
    parser.add_argument("--training-only", action="store_true", help="do not evaluate")

    parser.add_argument(
        "--no-checkpoints",
        action="store_false",
        dest="save_checkpoints",
        help="do not store any checkpoints, useful for benchmarking",
    )

    parser.add_argument("--checkpoint-filename", default="checkpoint.pth.tar", type=str)
<<<<<<< HEAD
    
=======

>>>>>>> repo1
    parser.add_argument(
        "--workspace",
        type=str,
        default="./",
        metavar="DIR",
        help="path to directory where checkpoints will be stored",
    )
    parser.add_argument(
        "--memory-format",
        type=str,
        default="nchw",
        choices=["nchw", "nhwc"],
        help="memory layout, nchw or nhwc",
    )
<<<<<<< HEAD


def main(args):
    exp_start_time = time.time()
    global best_prec1
    best_prec1 = 0
=======
    parser.add_argument("--use-ema", default=None, type=float, help="use EMA")
    parser.add_argument(
        "--augmentation",
        type=str,
        default=None,
        choices=[None, "autoaugment"],
        help="augmentation method",
    )


def prepare_for_training(args, model_args, model_arch):
>>>>>>> repo1

    args.distributed = False
    if "WORLD_SIZE" in os.environ:
        args.distributed = int(os.environ["WORLD_SIZE"]) > 1
        args.local_rank = int(os.environ["LOCAL_RANK"])
<<<<<<< HEAD
=======
    else:
        args.local_rank = 0
>>>>>>> repo1

    args.gpu = 0
    args.world_size = 1

    if args.distributed:
        args.gpu = args.local_rank % torch.cuda.device_count()
        torch.cuda.set_device(args.gpu)
        dist.init_process_group(backend="nccl", init_method="env://")
        args.world_size = torch.distributed.get_world_size()

<<<<<<< HEAD
    if args.amp and args.fp16:
        print("Please use only one of the --fp16/--amp flags")
        exit(1)

=======
>>>>>>> repo1
    if args.seed is not None:
        print("Using seed = {}".format(args.seed))
        torch.manual_seed(args.seed + args.local_rank)
        torch.cuda.manual_seed(args.seed + args.local_rank)
        np.random.seed(seed=args.seed + args.local_rank)
        random.seed(args.seed + args.local_rank)

        def _worker_init_fn(id):
            np.random.seed(seed=args.seed + args.local_rank + id)
            random.seed(args.seed + args.local_rank + id)

    else:

        def _worker_init_fn(id):
            pass

<<<<<<< HEAD
    if args.fp16:
        assert (
            torch.backends.cudnn.enabled
        ), "fp16 mode requires cudnn backend to be enabled."

    if args.static_loss_scale != 1.0:
        if not args.fp16:
            print("Warning:  if --fp16 is not used, static_loss_scale will be ignored.")
=======
    if args.static_loss_scale != 1.0:
        if not args.amp:
            print("Warning: if --amp is not used, static_loss_scale will be ignored.")
>>>>>>> repo1

    if args.optimizer_batch_size < 0:
        batch_size_multiplier = 1
    else:
        tbs = args.world_size * args.batch_size
        if args.optimizer_batch_size % tbs != 0:
            print(
                "Warning: simulated batch size {} is not divisible by actual batch size {}".format(
                    args.optimizer_batch_size, tbs
                )
            )
        batch_size_multiplier = int(args.optimizer_batch_size / tbs)
        print("BSM: {}".format(batch_size_multiplier))

<<<<<<< HEAD
    pretrained_weights = None
    if args.pretrained_weights:
        if os.path.isfile(args.pretrained_weights):
            print(
                "=> loading pretrained weights from '{}'".format(
                    args.pretrained_weights
                )
            )
            pretrained_weights = torch.load(args.pretrained_weights)
        else:
            print("=> no pretrained weights found at '{}'".format(args.resume))

=======
>>>>>>> repo1
    start_epoch = 0
    # optionally resume from a checkpoint
    if args.resume is not None:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(
                args.resume, map_location=lambda storage, loc: storage.cuda(args.gpu)
            )
            start_epoch = checkpoint["epoch"]
            best_prec1 = checkpoint["best_prec1"]
            model_state = checkpoint["state_dict"]
            optimizer_state = checkpoint["optimizer"]
<<<<<<< HEAD
=======
            if "state_dict_ema" in checkpoint:
                model_state_ema = checkpoint["state_dict_ema"]
>>>>>>> repo1
            print(
                "=> loaded checkpoint '{}' (epoch {})".format(
                    args.resume, checkpoint["epoch"]
                )
            )
<<<<<<< HEAD
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))
            model_state = None
            optimizer_state = None
    else:
        model_state = None
=======
            if start_epoch >= args.epochs:
                print(
                    f"Launched training for {args.epochs}, checkpoint already run {start_epoch}"
                )
                exit(1)
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))
            model_state = None
            model_state_ema = None
            optimizer_state = None
    else:
        model_state = None
        model_state_ema = None
>>>>>>> repo1
        optimizer_state = None

    loss = nn.CrossEntropyLoss
    if args.mixup > 0.0:
        loss = lambda: NLLMultiLabelSmooth(args.label_smoothing)
    elif args.label_smoothing > 0.0:
        loss = lambda: LabelSmoothing(args.label_smoothing)

    memory_format = (
        torch.channels_last if args.memory_format == "nhwc" else torch.contiguous_format
    )
<<<<<<< HEAD

    model_and_loss = ModelAndLoss(
        (args.arch, args.model_config, args.num_classes),
        loss,
        pretrained_weights=pretrained_weights,
        cuda=True,
        fp16=args.fp16,
        memory_format=memory_format,
    )
=======
    model = model_arch(
        **{
            k: v
            if k != "pretrained"
            else v and (not args.distributed or dist.get_rank() == 0)
            for k, v in model_args.__dict__.items()
        }
    )

    image_size = (
        args.image_size
        if args.image_size is not None
        else model.arch.default_image_size
    )
    model_and_loss = ModelAndLoss(model, loss, cuda=True, memory_format=memory_format)
    if args.use_ema is not None:
        model_ema = deepcopy(model_and_loss)
        ema = EMA(args.use_ema)
    else:
        model_ema = None
        ema = None
>>>>>>> repo1

    # Create data loaders and optimizers as needed
    if args.data_backend == "pytorch":
        get_train_loader = get_pytorch_train_loader
        get_val_loader = get_pytorch_val_loader
    elif args.data_backend == "dali-gpu":
        get_train_loader = get_dali_train_loader(dali_cpu=False)
        get_val_loader = get_dali_val_loader()
    elif args.data_backend == "dali-cpu":
        get_train_loader = get_dali_train_loader(dali_cpu=True)
        get_val_loader = get_dali_val_loader()
    elif args.data_backend == "syntetic":
        get_val_loader = get_syntetic_loader
        get_train_loader = get_syntetic_loader
<<<<<<< HEAD

    train_loader, train_loader_len = get_train_loader(
        args.data,
        args.batch_size,
        args.num_classes,
        args.mixup > 0.0,
        start_epoch=start_epoch,
        workers=args.workers,
        fp16=args.fp16,
=======
    else:
        print("Bad databackend picked")
        exit(1)

    train_loader, train_loader_len = get_train_loader(
        args.data,
        image_size,
        args.batch_size,
        model_args.num_classes,
        args.mixup > 0.0,
        interpolation = args.interpolation,
        augmentation=args.augmentation,
        start_epoch=start_epoch,
        workers=args.workers,
>>>>>>> repo1
        memory_format=memory_format,
    )
    if args.mixup != 0.0:
        train_loader = MixUpWrapper(args.mixup, train_loader)

    val_loader, val_loader_len = get_val_loader(
        args.data,
<<<<<<< HEAD
        args.batch_size,
        args.num_classes,
        False,
        workers=args.workers,
        fp16=args.fp16,
=======
        image_size,
        args.batch_size,
        model_args.num_classes,
        False,
        interpolation = args.interpolation,
        workers=args.workers,
>>>>>>> repo1
        memory_format=memory_format,
    )

    if not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0:
        logger = log.Logger(
            args.print_freq,
            [
                dllogger.StdOutBackend(
                    dllogger.Verbosity.DEFAULT, step_format=log.format_step
                ),
                dllogger.JSONStreamBackend(
                    dllogger.Verbosity.VERBOSE,
                    os.path.join(args.workspace, args.raport_file),
                ),
            ],
            start_epoch=start_epoch - 1,
        )

    else:
        logger = log.Logger(args.print_freq, [], start_epoch=start_epoch - 1)

    logger.log_parameter(args.__dict__, verbosity=dllogger.Verbosity.DEFAULT)
<<<<<<< HEAD

    optimizer = get_optimizer(
        list(model_and_loss.model.named_parameters()),
        args.fp16,
        args.lr,
        args.momentum,
        args.weight_decay,
        nesterov=args.nesterov,
        bn_weight_decay=args.bn_weight_decay,
        state=optimizer_state,
        static_loss_scale=args.static_loss_scale,
        dynamic_loss_scale=args.dynamic_loss_scale,
=======
    logger.log_parameter(
        {f"model.{k}": v for k, v in model_args.__dict__.items()},
        verbosity=dllogger.Verbosity.DEFAULT,
    )

    optimizer = get_optimizer(
        list(model_and_loss.model.named_parameters()),
        args.lr,
        args=args,
        state=optimizer_state,
>>>>>>> repo1
    )

    if args.lr_schedule == "step":
        lr_policy = lr_step_policy(
            args.lr, [30, 60, 80], 0.1, args.warmup, logger=logger
        )
    elif args.lr_schedule == "cosine":
<<<<<<< HEAD
        lr_policy = lr_cosine_policy(args.lr, args.warmup, args.epochs, logger=logger)
    elif args.lr_schedule == "linear":
        lr_policy = lr_linear_policy(args.lr, args.warmup, args.epochs, logger=logger)

    if args.amp:
        model_and_loss, optimizer = amp.initialize(
            model_and_loss,
            optimizer,
            opt_level="O1",
            loss_scale="dynamic" if args.dynamic_loss_scale else args.static_loss_scale,
        )

    if args.distributed:
        model_and_loss.distributed()

    model_and_loss.load_model_state(model_state)
=======
        lr_policy = lr_cosine_policy(
            args.lr, args.warmup, args.epochs, end_lr=args.end_lr, logger=logger
        )
    elif args.lr_schedule == "linear":
        lr_policy = lr_linear_policy(args.lr, args.warmup, args.epochs, logger=logger)

    scaler = torch.cuda.amp.GradScaler(
        init_scale=args.static_loss_scale,
        growth_factor=2,
        backoff_factor=0.5,
        growth_interval=100 if args.dynamic_loss_scale else 1000000000,
        enabled=args.amp,
    )

    if args.distributed:
        model_and_loss.distributed(args.gpu)

    model_and_loss.load_model_state(model_state)
    if (ema is not None) and (model_state_ema is not None):
        print("load ema")
        ema.load_state_dict(model_state_ema)

    return (model_and_loss, optimizer, lr_policy, scaler, train_loader, val_loader, logger, ema, model_ema,
            train_loader_len, batch_size_multiplier, start_epoch)


def main(args, model_args, model_arch):
    exp_start_time = time.time()
    global best_prec1
    best_prec1 = 0

    model_and_loss, optimizer, lr_policy, scaler, train_loader, val_loader, logger, ema, model_ema, train_loader_len, \
        batch_size_multiplier, start_epoch = prepare_for_training(args, model_args, model_arch)
>>>>>>> repo1

    train_loop(
        model_and_loss,
        optimizer,
<<<<<<< HEAD
        lr_policy,
        train_loader,
        val_loader,
        args.fp16,
        logger,
        should_backup_checkpoint(args),
        use_amp=args.amp,
        batch_size_multiplier=batch_size_multiplier,
        start_epoch=start_epoch,
        end_epoch=(start_epoch + args.run_epochs)
        if args.run_epochs != -1
        else args.epochs,
=======
        scaler,
        lr_policy,
        train_loader,
        val_loader,
        logger,
        should_backup_checkpoint(args),
        ema=ema,
        model_ema=model_ema,
        steps_per_epoch=train_loader_len,
        use_amp=args.amp,
        batch_size_multiplier=batch_size_multiplier,
        start_epoch=start_epoch,
        end_epoch=min((start_epoch + args.run_epochs), args.epochs)
        if args.run_epochs != -1
        else args.epochs,
        early_stopping_patience=args.early_stopping_patience,
>>>>>>> repo1
        best_prec1=best_prec1,
        prof=args.prof,
        skip_training=args.evaluate,
        skip_validation=args.training_only,
        save_checkpoints=args.save_checkpoints and not args.evaluate,
        checkpoint_dir=args.workspace,
        checkpoint_filename=args.checkpoint_filename,
    )
    exp_duration = time.time() - exp_start_time
    if not torch.distributed.is_initialized() or torch.distributed.get_rank() == 0:
        logger.end()
    print("Experiment ended")


if __name__ == "__main__":
<<<<<<< HEAD
    parser = argparse.ArgumentParser(description="PyTorch ImageNet Training")

    add_parser_arguments(parser)
    args = parser.parse_args()
    cudnn.benchmark = True

    main(args)
=======

    epilog = [
        "Based on the architecture picked by --arch flag, you may use the following options:\n"
    ]
    for model, ep in available_models().items():
        model_help = "\n".join(ep.parser().format_help().split("\n")[2:])
        epilog.append(model_help)
    parser = argparse.ArgumentParser(
        description="PyTorch ImageNet Training",
        epilog="\n".join(epilog),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_parser_arguments(parser)

    args, rest = parser.parse_known_args()
    
    model_arch = available_models()[args.arch]
    model_args, rest = model_arch.parser().parse_known_args(rest)
    print(model_args)

    assert len(rest) == 0, f"Unknown args passed: {rest}"

    cudnn.benchmark = True

    main(args, model_args, model_arch)
>>>>>>> repo1