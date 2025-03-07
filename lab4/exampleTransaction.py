example_transaction = {
    "type": 1,
    "input": {
        "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
        "n": 0,
    },
    "sig": "674a8311d10d4dd6fd1d5bb4b9d27a5ea48acad066784e6b3505d02d88fc4a690ff20d478de6a5535d3491a2fb62a929",
    "output": [
        {
            "value": 25,
            "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
        }
    ],
}

example_blockchain = [
    {
        "type": 0,
        "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
        "nonce": "1950b006f9203221515467fe14765720",
        "pow": "00000027e2eb250f341b05ffe24f43adae3b8181739cd976ea263a4ae0ff8eb7",
        "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
        "tx": {
            "type": 1,
            "input": {
                "id": "0000000000000000000000000000000000000000000000000000000000000000",
                "n": 0,
            },
            "sig": "adf494f10d30814fd26c6f0e1b2893d0fb3d037b341210bf23ef9705479c7e90879f794a29960d3ff13b50ecd780c872",
            "output": [
                {
                    "value": 50,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                }
            ],
        },
    },
    {
        "type": 0,
        "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
        "nonce": "a3ce6c333e8b1af83bcf07f847a37db1",
        "pow": "000000429675a2c5f52756f1630eed4b596fa93a25d69f61beb8d6feaff18916",
        "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
        "tx": {
            "type": 1,
            "input": {
                "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
                "n": 0,
            },
            "sig": "ca0ebbc83ac5777f12f727d1cb9ef77d1daf6b152aac3f8c58f376ffccfeb40bebed17d732b9ebeb56468c66e7b8105f",
            "output": [
                {
                    "value": 25,
                    "pub_key": "366bd531ff0767ccd59764a85c9cdbd3645377bff56caf18657bad154aa9890ca6942db5f8ac23eeb50cda327ea6bec4",
                },
                {
                    "value": 25,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
                {
                    "value": 50,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "6ffabedafcc2de43bc36075a35339f200b51bf49a35a39f696f86cde470aaccf",
        "nonce": "1b043557fd01b0d913ef37c131ea0770",
        "pow": "0000003924f722d046f68666b2f6bb24dc9da129e335ce3110da7f8583956e69",
        "prev": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
        "tx": {
            "type": 1,
            "input": {
                "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
                "n": 1,
            },
            "sig": "aaa0a47a6f5b827de876cae48e3838d0f4fbbc83548f1ee0006df27eb043a380e8d85fc262f86db7099747961a5fd17f",
            "output": [
                {
                    "value": 25,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
                {
                    "value": 50,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "cecc7104e06573e36670c4475c57547163f3f0a8eca842f274a2fcc1a9f668b0",
        "nonce": "f3cdf800860fe73678ce5758d9c78cac",
        "pow": "0000006890c92eb31559ad6916df52270e1d54dca5c11c61021328a1d2409911",
        "prev": "6ffabedafcc2de43bc36075a35339f200b51bf49a35a39f696f86cde470aaccf",
        "tx": {
            "type": 1,
            "input": {
                "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
                "n": 0,
            },
            "sig": "6273821392947a6a4f57f77332850664a192aa94a179f16cc7f7a53129c3bc3c7f36da06e73c3233042b6fcdbfb60bb2",
            "output": [
                {
                    "value": 1,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 24,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "219481926209462eb9d7caea8b44eb44132d077ad0823e6e7bd38e105b51af3a",
        "nonce": "82c4c3fe511dba19f073ccb0a1c774f8",
        "pow": "0000003dcbbd44921a4d2ceeb514e92d11d85eedefc2646ad6e4e495b2d69a59",
        "prev": "cecc7104e06573e36670c4475c57547163f3f0a8eca842f274a2fcc1a9f668b0",
        "tx": {
            "type": 1,
            "input": {
                "id": "cecc7104e06573e36670c4475c57547163f3f0a8eca842f274a2fcc1a9f668b0",
                "n": 0,
            },
            "sig": "c14a38ce3f09124ae0428c3525f013b4bc5f53532fb0838685feb696b51f2a1a9eb100cc858425ee0d586c17802c458e",
            "output": [
                {
                    "value": 1,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "c622791467a43dd8bf77206b20310ffb0aa8b6ce8be76f55c6e0a05aa3adfefb",
        "nonce": "27abb4cc56f4c109cac2a366d9d9e505",
        "pow": "00000028c54db8bf69f44c57397cc0abaf9ed8ef0f0259e4f4024a57058c5c6e",
        "prev": "219481926209462eb9d7caea8b44eb44132d077ad0823e6e7bd38e105b51af3a",
        "tx": {
            "type": 1,
            "input": {
                "id": "219481926209462eb9d7caea8b44eb44132d077ad0823e6e7bd38e105b51af3a",
                "n": 1,
            },
            "sig": "a4a8fba853b89d1a85d0bc5da2bb90fc0c8279bcdf9c67faa95d38c8cc2b2d0ecf8c06b44f635863eda4fcc85b8d4441",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "3c11f8e4cfc9a858f5faba1d0d5665bca6f618eb02cdf7420e079f75e0a05e91",
        "nonce": "e2f7783f9e88455e40bf5719c078d222",
        "pow": "00000042a55be1bc9e358f9b50828d218c3f63198e2ee88e482a8ccd6084b2ee",
        "prev": "c622791467a43dd8bf77206b20310ffb0aa8b6ce8be76f55c6e0a05aa3adfefb",
        "tx": {
            "type": 1,
            "input": {
                "id": "c622791467a43dd8bf77206b20310ffb0aa8b6ce8be76f55c6e0a05aa3adfefb",
                "n": 1,
            },
            "sig": "57532dc4ed53a0a6e7ac2b2083ca11aa7fe610d82973afd04c692910ca27c8ea43721e930087e11b9110f85687682470",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "9e8f32a96bec5a51c8233f5a9c6aabbcb6cf48303f22f8db27737bed75a719a2",
        "nonce": "7d15fa0470b717953c8890104cf91060",
        "pow": "0000002ae80eea5bbaebdf1515f01e18d2ff5fd773ad93edd4380c03414b3c60",
        "prev": "3c11f8e4cfc9a858f5faba1d0d5665bca6f618eb02cdf7420e079f75e0a05e91",
        "tx": {
            "type": 1,
            "input": {
                "id": "3c11f8e4cfc9a858f5faba1d0d5665bca6f618eb02cdf7420e079f75e0a05e91",
                "n": 1,
            },
            "sig": "f9fe5d6a83a693dc33fb998f0f703ce83782e1d310458c8be8c62395e987431e586433c642183a73c8747202a22f18a2",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "dde40d5ad4089aa57b55712af3ed7c428317f09e9ff419d16ab94aa9157958dd",
        "nonce": "ec9294c0a96ab590eddb5883614a5c07",
        "pow": "0000003a8c40a207a48d1b4563d392c98218a4da4ebcb04790047dd57b71f636",
        "prev": "9e8f32a96bec5a51c8233f5a9c6aabbcb6cf48303f22f8db27737bed75a719a2",
        "tx": {
            "type": 1,
            "input": {
                "id": "9e8f32a96bec5a51c8233f5a9c6aabbcb6cf48303f22f8db27737bed75a719a2",
                "n": 1,
            },
            "sig": "016d9be68e21d5041d4f32e567d08950abbcc6cae0050d8c0a5f8f0eca61a6ebaad83a48210916dbf8698ecbe5778c51",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "ea12d20992351532419654816d7310edca91716b1f274ac273cc9e867b94712d",
        "nonce": "ecda964ff232eadd2449429b9fa1ea17",
        "pow": "00000062ea6879c486a91a2bf349d1eee51a59021ab6819b72b60bb9cb326d2e",
        "prev": "dde40d5ad4089aa57b55712af3ed7c428317f09e9ff419d16ab94aa9157958dd",
        "tx": {
            "type": 1,
            "input": {
                "id": "dde40d5ad4089aa57b55712af3ed7c428317f09e9ff419d16ab94aa9157958dd",
                "n": 1,
            },
            "sig": "9dc03783f125f9d2f5cac5b9b3c260c552ba949b4a3adb02d1ed4587f1c6fcc111476a9c9385ef4a6d9440d529ae5810",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "fdcce4c540b304ad18440175a77c6c036ba6c1e8d35294928a10550223a8f238",
        "nonce": "37e4ac153d1dfed605c081f37947a564",
        "pow": "0000007febbce470237829bbe2b150f389a3d1ce3398926ff7aa366072d22ad8",
        "prev": "ea12d20992351532419654816d7310edca91716b1f274ac273cc9e867b94712d",
        "tx": {
            "type": 1,
            "input": {
                "id": "ea12d20992351532419654816d7310edca91716b1f274ac273cc9e867b94712d",
                "n": 1,
            },
            "sig": "60f76966d54f479388bd7ced21e6ac737d2fcfd7ec9e3eb685ecf3e56dff56d308a9189386cdafe189880e10f8e659f1",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "e9966038cf9521424ab446f3683da293b98dea5c809905c79c7b6b4cb8ab50bf",
        "nonce": "606d479706b074f445e30c1af7d6a4ec",
        "pow": "0000004e23686e1ff81ef12e49bc165b5493ae6fa5d8df56b784c22126910e34",
        "prev": "fdcce4c540b304ad18440175a77c6c036ba6c1e8d35294928a10550223a8f238",
        "tx": {
            "type": 1,
            "input": {
                "id": "fdcce4c540b304ad18440175a77c6c036ba6c1e8d35294928a10550223a8f238",
                "n": 1,
            },
            "sig": "589e2121f20497123c4b84cdec0fc7be6de4713d68d7896f688e08739ee18da7bdfb00c0c5b4473affd4a25c8ccb5dea",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "05b6e246efc688424f8eb6e1071b1d455f1eb871e4c4492aa211de5b6e86a91d",
        "nonce": "d50eb62d69a8b29315300e1b879ed18e",
        "pow": "00000060f5656936fbc2efb90310545d72162ad3dfb90cac2e9f9e5b1d8befdf",
        "prev": "e9966038cf9521424ab446f3683da293b98dea5c809905c79c7b6b4cb8ab50bf",
        "tx": {
            "type": 1,
            "input": {
                "id": "e9966038cf9521424ab446f3683da293b98dea5c809905c79c7b6b4cb8ab50bf",
                "n": 1,
            },
            "sig": "d72b4aed950bcf34330548f032605fb521fe2a22c9943a41e26d0901c4992298822aa52ffbc20ff6600f80afae5c52e6",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "a916e102bbd0aad93e47ec3007cf923f22b2eff1587215787e5184bc0705dd3e",
        "nonce": "6dc6d4bb45f357eaa99bdb341366e802",
        "pow": "0000005d4bc891144a536f8b7f1a81f9e307ce8c21deaa7d15a17d84582ab550",
        "prev": "05b6e246efc688424f8eb6e1071b1d455f1eb871e4c4492aa211de5b6e86a91d",
        "tx": {
            "type": 1,
            "input": {
                "id": "05b6e246efc688424f8eb6e1071b1d455f1eb871e4c4492aa211de5b6e86a91d",
                "n": 1,
            },
            "sig": "b031bbda8b23a1dbb6483c44ddc2ae68dc4725aab115b60ecbc2e4066c4e95acd74d77bae8afefd9b7121587dcb73f50",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "9e95958ec4b90991af93c1d35fbc027ff9f9b06b3d333a7e9d915d728407ba47",
        "nonce": "990cbbb920a94dc511108b233797515d",
        "pow": "000000192b25405e6d1ec5a066d128c33399fb102455803f085ce0086c28b158",
        "prev": "a916e102bbd0aad93e47ec3007cf923f22b2eff1587215787e5184bc0705dd3e",
        "tx": {
            "type": 1,
            "input": {
                "id": "a916e102bbd0aad93e47ec3007cf923f22b2eff1587215787e5184bc0705dd3e",
                "n": 1,
            },
            "sig": "d65abee1fd467091603275da6c0c3896553aa1c2a787ec2690ffdc3768e3faa11fb8d37549a9128b9eb353fbcb6a0a9a",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "c73e6b1438b817d6afe1eb8736a00492fcf166edf05fc6564c8e82a99f748e62",
        "nonce": "52fe7dfa9928a5cf0812ebb5f935ec70",
        "pow": "0000004e6691a628c483982ebc620b89ae1ea1919e0052b3d47ef70aa2bb84ba",
        "prev": "9e95958ec4b90991af93c1d35fbc027ff9f9b06b3d333a7e9d915d728407ba47",
        "tx": {
            "type": 1,
            "input": {
                "id": "9e95958ec4b90991af93c1d35fbc027ff9f9b06b3d333a7e9d915d728407ba47",
                "n": 1,
            },
            "sig": "6f9abda2207c877538d1391d5e0f02e948256880a21a2c4482a009899945be7b4a6b211ac6b11d0a1059bacfb176054b",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "50c398fe0059e637d297053c4c4db6d73da2341596480f37a732ec4088ff1993",
        "nonce": "690fe044c2ab40dba73d188b2af63c13",
        "pow": "0000003c8c3cbebf0ac6c24fb0abf9aebd5b58481a4563454b18e8fb668e7def",
        "prev": "c73e6b1438b817d6afe1eb8736a00492fcf166edf05fc6564c8e82a99f748e62",
        "tx": {
            "type": 1,
            "input": {
                "id": "c73e6b1438b817d6afe1eb8736a00492fcf166edf05fc6564c8e82a99f748e62",
                "n": 1,
            },
            "sig": "346142727a2f87aa2fe37c1c228d362b56f7156f9b4ce93dc5bf468cb7f4e353ee34c897e76377e4aea956f8acf35ff6",
            "output": [
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "7dc68d4134d544b4e7dd7d6672134cbe7f2e09cbd7ee24331d6fa10a0ff1c2d4",
        "nonce": "4a59eebe32d2ff7f8ed6b34a78b7fead",
        "pow": "0000000c4ce5a414489a425c7be2a904625d9925c019b87975a795150a3b5b66",
        "prev": "50c398fe0059e637d297053c4c4db6d73da2341596480f37a732ec4088ff1993",
        "tx": {
            "type": 1,
            "input": {
                "id": "aa31fb4ef777b9e3e0cbeccba6ff58b5b2fecb61b6902f4f4561f7291fcad17c",
                "n": 2,
            },
            "sig": "184841841d94d3db7dde18b9b8f6ef3e1238733df37a040f7234f0e11c7e53a6651177aa7c0ffe9f7931c8bfae726545",
            "output": [
                {
                    "value": 25,
                    "pub_key": "856e98824150ae0175ba799a8d3eae6ad7bbe5c7e9b4c409027d35cf6d2690960e2a5c1b5573c9e8a0e579b7cd18cb2b",
                },
                {
                    "value": 25,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
                {
                    "value": 50,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "7dd7602f07ed567675502e183fee920ddb5d0eb8cc713e8531179937e0c321f0",
        "nonce": "f541329d00356356420c3c162f09dae4",
        "pow": "000000133d5a22798632362437c3f82c030a22a3e95a46270b5557230cfec03f",
        "prev": "7dc68d4134d544b4e7dd7d6672134cbe7f2e09cbd7ee24331d6fa10a0ff1c2d4",
        "tx": {
            "type": 1,
            "input": {
                "id": "50c398fe0059e637d297053c4c4db6d73da2341596480f37a732ec4088ff1993",
                "n": 1,
            },
            "sig": "bbaa6a428e3aad8025e6970db00f7d52aa23b4a5c12f7b98100342ba40d6c807cf30ec29acc37a3f1c6afa27711ed869",
            "output": [
                {
                    "value": 1,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
                {
                    "value": 49,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
                {
                    "value": 50,
                    "pub_key": "825f8bdb84e691f8a0ff1f4b65aadb0dc036cd006672653ff77f3dbc4667c85aded761de13e115708e03f66c1e327b69",
                },
            ],
        },
    },
    {
        "type": 0,
        "id": "842096e5bc909c30779e07960ef7f3c7ab7c359dfc7a7130f83e3a5ad37e4fab",
        "nonce": "ec2ada8cb9fe5df71432d2f8e2a7ee14",
        "pow": "0000002449571dbf6b9916a8a3cd8ffc71d9f6f7d9932e39d61bbc4b9ae98416",
        "prev": "7dd7602f07ed567675502e183fee920ddb5d0eb8cc713e8531179937e0c321f0",
        "tx": {
            "type": 1,
            "input": {
                "id": "6ffabedafcc2de43bc36075a35339f200b51bf49a35a39f696f86cde470aaccf",
                "n": 0,
            },
            "sig": "58ce3d9317bf4f3b4d29fcb8dd0493833bb5db9b944e0d9efffe4b3b06e7d9d98023ed7b81ed9dbfb6adad980d830f0e",
            "output": [
                {
                    "value": 25,
                    "pub_key": "363b9615cc7fa2c597ed9fe156dd91920fd1598ce4a896e6cfda2dd9cc15c9e8be5709e84683e6215505d93510826987",
                },
                {
                    "value": 50,
                    "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa",
                },
            ],
        },
    },
]
